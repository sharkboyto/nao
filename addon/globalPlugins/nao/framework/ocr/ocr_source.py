#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-26
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os

class OCRSource:
	SOURCE_TYPE_UWP_OCR = 'uwp_ocr'

	def __init__(self, type, file=None, language=None, converter_version=None, original_file=None, on_source_file_hash_finish=None):
		from threading import Lock
		from .. generic.version import addon_version
		self._hash_lock = Lock()
		self._async_hash_result = None
		self.clear()
		self.type = type
		self.file = file
		self.language = language
		self.converter = converter_version
		self.addon = addon_version()
		if original_file:
			self.original_file = original_file
		else:
			self.original_file = file
		if self.file:
			try:
				self.file_size = os.stat(self.file).st_size
			except:
				self.file_size = None
		self.source_file_async_hash(on_finish=on_source_file_hash_finish)

	def clear(self):
		if self._async_hash_result:
			self._async_hash_result.terminate()
			self._async_hash_result.wait()
		self.file = None
		self.file_size = None
		self.language = None
		self.converter = None
		self.addon = None
		self._file_hash = None
		self._hash = None

	def dictionary(self):
		file_hash = self.FileHash
		hash = self.Hash
		ret = {'type': self.type}
		if self.original_file: ret['file'] = self.original_file
		if self.file_size is not None: ret['file_size'] = self.file_size
		if self.language: ret['language'] = self.language
		if self.converter: ret['converter'] = self.converter
		if self.addon: ret['addon'] = self.addon
		if file_hash: ret['file_hash'] = file_hash
		if hash: ret['hash'] = hash
		return ret

	def from_dictionary(value):
		ret = None
		if value and 'type' in value:
			if value['type'] == OCRSource.SOURCE_TYPE_UWP_OCR:
				ret = UWPOCRSource(file=None, language=None).parse_dictionary(value)
		return ret

	def parse_dictionary(self, value):
		self.clear()
		if value:
			if 'file' in value: self.file = self.original_file = value['file']
			if 'file_size' in value: self.file_size = value['file_size']
			if 'language' in value: self.language = value['language']
			if 'converter' in value: self.converter = value['converter']
			if 'addon' in value: self.addon = value['addon']
			if 'file_hash' in value or 'hash' in value:
				self._hash_lock.acquire()
				if 'file_hash' in value: self._file_hash = value['file_hash']
				if 'hash' in value: self._hash = value['hash']
				self._hash_lock.release()
		return self

	def base_hash_update(self, md):
		md.update_string(self.type, self.language, self.converter)
		if self.file_size is None:
			md.update_long_long(-1)
		else:
			md.update_long_long(self.file_size)

	def hash_update(self, md):
		self.base_hash_update(md)
		md.update_string(self.original_file, self.FileHash, self.Hash)
		if self.addon:
			from .. generic.version import addon_version_hash_update
			addon_version_hash_update(md, self.addon)
		else:
			md.update_char(0)

	def source_file_async_hash(self, use_lock=True, on_finish=None):
		from .. generic.md import MessageDigest
		from .. threading import AsyncCall
		if use_lock: self._hash_lock.acquire()
		self._file_hash = None
		self._hash = None
		if self.file and os.path.isfile(self.file):
			def h(result):
				if result.Value and result.Value.status == True:
					self._file_hash = result.Value.md.digest().hex()
					self.base_hash_update(result.Value.md)
					self._hash = result.Value.md.digest().hex()
				if use_lock: self._hash_lock.release()
				if on_finish: AsyncCall(on_finish, source=self, status=result.Value and result.Value.status == True)
			self._async_hash_result = MessageDigest('sha256').update_file_async(self.file, h)	
		else:
			if use_lock: self._hash_lock.release()
			if on_finish: AsyncCall(on_finish, source=self, status=False)

	def match_with(self, source):
		#this is not an equals method. Match if source file and recognition parameters are the same
		if not source: return False
		if source.FileHash != self.FileHash: return False
		if source.Hash != self.Hash: return False
		if source.type != self.type: return False
		if source.language != self.language: return False
		if source.converter != self.converter: return False
		if source.file_size != self.file_size: return False
		return True

	@property
	def FileHash(self):
		self._hash_lock.acquire()
		ret = self._file_hash
		if not ret and not self._async_hash_result:
			self.source_file_async_hash(use_lock=False)
			if self._async_hash_result:
				self._async_hash_result.wait()
				ret = self._file_hash
		self._hash_lock.release()
		return ret

	@property
	def Hash(self):
		self.FileHash
		self._hash_lock.acquire()
		ret = self._hash
		self._hash_lock.release()
		return ret

class UWPOCRSource(OCRSource):
	def __init__(self, file, language, converter_version=None, original_file=None, on_source_file_hash_finish=None):
		super(UWPOCRSource, self).__init__(type=OCRSource.SOURCE_TYPE_UWP_OCR, file=file, language=language, converter_version=converter_version, original_file=original_file, on_source_file_hash_finish=on_source_file_hash_finish)