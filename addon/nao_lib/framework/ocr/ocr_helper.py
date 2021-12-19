#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-19
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import addonHandler
from . ocr import OCR
from . ocr_result import OCRResultDialog
from .. speech import speech
from .. generic.beepThread import BeepThread
from .. converters.pdf_converter import PDFConverter
from .. converters.webp_converter import WebpConverter

addonHandler.initTranslation()

class OCRHelper:
	def __init__(self):
		self.supported_extensions = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp"]
		self.beeper = BeepThread()

	def recognize_file(self, source_file):
		if not source_file:
			return False
		if not OCR.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.message(_("Windows OCR not available"))
			return False
		# Getting the extension to check if is a supported file type.
		file_extension = os.path.splitext(source_file)[1].lower()
		if file_extension and file_extension.startswith('.'):
			file_extension = file_extension[1:]
		if not file_extension or not (file_extension in self.supported_extensions):
			speech.message(_("File not supported"))
			return False
		
		def recognize_finish(source_file, result, pages_offset, arg=None):
			self.beeper.stop()
			speech.cancel()
			if result and not isinstance(result, Exception):
				OCRResultDialog(source_file=source_file, result=result, pages_offset=pages_offset)
		
		speech.message(_("Process started"))
		self.beeper.start()
		if file_extension == 'pdf':
			conv = PDFConverter()
		elif file_extension == 'webp':
			conv = WebpConverter()
		else:
			OCR().recognize_files(source_file, [source_file], recognize_finish)
			return True
		def on_convert(success, converter):
			if success:
				OCR().recognize_files(converter.source_file, converter.results, recognize_finish, conv)
			else:
				speech.queue_message(_("Error, the file could not be processed."))
				self.beeper.stop()
		conv.to_png(source_file, on_convert)
		return True