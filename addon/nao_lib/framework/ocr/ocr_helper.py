#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-21
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import gui
from . ocr import OCR
from . ocr_progress import OCRProgressDialog
from . ocr_result import OCRResultDialog
from .. speech import speech
from .. import language
from .. generic.beepThread import BeepThread
from .. converters.pdf_converter import PDFConverter
from .. converters.webp_converter import WebpConverter

language.initTranslation()

class OCRHelper:
	def __init__(self):
		self.supported_extensions = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp"]
		self.beeper = BeepThread()
		self.progress_timeout = 5

	def recognize_screenshot():
		def recognize_start():
			# Translators: Reporting when recognition (e.g. OCR) begins.
			speech.queue_message(_N("Recognizing"))
		OCR.recognize_screenshot(on_start=recognize_start)

	def recognize_file(self, source_file):
		if not source_file:
			return False
		if not OCR.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.message(_N("Windows OCR not available"))
			return False
		# Getting the extension to check if is a supported file type.
		file_extension = os.path.splitext(source_file)[1].lower()
		if file_extension and file_extension.startswith('.'):
			file_extension = file_extension[1:]
		if not file_extension or not (file_extension in self.supported_extensions):
			# Translators: Reported when the file format is not supported for recognition.
			speech.message(_("File not supported"))
			return False
		
		conv = None
		ocr = OCR()
		progress = None
		on_convert_progress = None
		on_recognize_start = None
		on_recognize_progress = None
		if file_extension == 'pdf':
			conv = PDFConverter()
			def on_cancel():
				conv.abort()
				ocr.abort()
			# Translators: Reporting when recognition (e.g. OCR) begins.
			progress = OCRProgressDialog(title=_N("Recognizing") + ' ' + os.path.basename(source_file), on_cancel=on_cancel)
			def on_convert_progress(conv, current, total):
				if current > 0:
					progress.tick(int(round(current / 2)), total, use_percentage=False)
			def on_recognize_progress(current, total):
				if current > 0:
					progress.tick(int(round((total + current) / 2)), total, use_percentage=False)
		elif file_extension == 'webp':
			conv = WebpConverter()
		
		if not progress:
			# Translators: Reported when the recognition starts.
			speech.message(_("Process started"))
			self.beeper.start()
			def on_recognize_start(source_file):
				# Translators: Reporting when recognition (e.g. OCR) begins.
				speech.queue_message(_N("Recognizing"))
		
		def on_recognize_finish(source_file, result, pages_offset, arg=None):
			self.beeper.stop()
			if progress:
				progress.Close()
			if result and not isinstance(result, Exception):
				speech.cancel()
				OCRResultDialog(source_file=source_file, result=result, pages_offset=pages_offset)
		
		if not conv:
			ocr.recognize_files(source_file, [source_file], on_start=on_recognize_start, on_finish=on_recognize_finish)
			return True
		
		def on_convert_finish(success, converter):
			if success:
				ocr.recognize_files(converter.source_file, converter.results, on_start=on_recognize_start, on_finish=on_recognize_finish, on_finish_arg=conv, on_progress=on_recognize_progress, progress_timeout=self.progress_timeout)
			else:
				if progress:
					progress.Close()
				self.beeper.stop()
				# Translators: Reported when unable to process a file for recognition.
				speech.queue_message(_("Error, the file could not be processed"))
		
		conv.to_png(source_file, on_convert_finish, on_convert_progress, self.progress_timeout)
		return True