#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

class OCRSource:
	SOURCE_TYPE_UWP_OCR = 'uwp_ocr'

	def __init__(self, type, file=None, language=None):
		self._type = type
		self.file = file
		self.language = language

	def dictionary(self):
		ret = {'type': self._type}
		if self.file: ret['file'] = self.file
		if self.language: ret['language'] = self.language
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
		return self

class UWPOCRSource(OCRSource):
	def __init__(self, file, language):
		super(UWPOCRSource, self).__init__(type=OCRSource.SOURCE_TYPE_UWP_OCR, file=file, language=language)