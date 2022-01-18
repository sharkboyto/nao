#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-18
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
from threading import Lock
from .. threading import AsyncResult

class OCRSource:
	SOURCE_TYPE_UWP_OCR = 'uwp_ocr'

	def __init__(self, type, file=None, language=None, file_hash_async_result=None):
		self._type = type
		self.file = file
		self.language = language
		self._file_hash_result = file_hash_async_result
		self._file_hash_lock = Lock()

	def clear(self):
		fhr = self._file_hash_result
		if fhr and isinstance(fhr, AsyncResult):
			fhr.terminate()
			fhr.wait()
		self._type = None
		self.file = None
		self.language = None
		self._file_hash_result = None

	def dictionary(self):
		hash = self.FileHash
		ret = {'type': self._type}
		if self.file: ret['file'] = self.file
		if self.language: ret['language'] = self.language
		if hash: ret['hash'] = hash
		return ret

	def from_dictionary(value):
		ret = None
		if value and 'type' in value:
			if value['type'] == OCRSource.SOURCE_TYPE_UWP_OCR:
				ret = UWPOCRSource(file=None, language=None).parse_dictionary(value)
		return ret

	def parse_dictionary(self, value):
		if value:
			if 'file' in value: self.file = value['file']
			if 'language' in value: self.language = value['language']
			if 'hash' in value:
				self._file_hash_lock.acquire()
				self._file_hash_result = value['hash']
				self._file_hash_lock.release()
		return self

	def hash(self, md):
		md.update_string(self._type, self.file, self.language, self.FileHash)

	@property
	def FileHash(self):
		self._file_hash_lock.acquire()
		ret = self._file_hash_result
		if ret and isinstance(ret, AsyncResult):
			ret.wait()
			if ret.Value and ret.Value.status == True:
				self._file_hash_result = ret.Value.md.digest().hex()
				ret = self._file_hash_result
			else:
				ret = None
		self._file_hash_lock.release()
		return ret

class UWPOCRSource(OCRSource):
	def __init__(self, file, language, file_hash_async_result=None):
		super(UWPOCRSource, self).__init__(type=OCRSource.SOURCE_TYPE_UWP_OCR, file=file, language=language, file_hash_async_result=file_hash_async_result)