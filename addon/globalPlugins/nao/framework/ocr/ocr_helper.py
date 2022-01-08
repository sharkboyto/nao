#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-07
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import gui
import wx
from . ocr import OCR, OCRMultipageSourceFile
from . ocr_service import OCRService
from . ocr_progress import OCRProgressDialog
from . ocr_result import OCRResultDialog
from .. speech import speech
from .. import language
from .. generic.beepThread import BeepThread
from .. converters.pdf_converter import PDFConverter
from .. converters.webp_converter import WebpConverter
from .. converters.djvu_converter import DjVuConverter

language.initTranslation()

class OCRHelper:
	def __init__(self):
		self.supported_extensions = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp", "djvu"]
		self.beeper = BeepThread()
		self.progress_timeout = 1

	def recognize_screenshot():
		def recognize_start():
			# Translators: Reporting when recognition (e.g. OCR) begins.
			speech.queue_message(_N("Recognizing"))
		OCR.recognize_screenshot(on_start=recognize_start)

	def recognize_file(self, source_file):
		if not source_file:
			return False
		if not OCRService.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.message(_N("Windows OCR not available"))
			return False
		# Getting the extension to check if is a supported file type.
		file_extension = OCR.get_file_extension(source_file)
		if not file_extension or not (file_extension in self.supported_extensions):
			# Translators: Reported when the file format is not supported for recognition.
			speech.message(_("File not supported"))
			return False
		
		conv = None
		ocr = OCR()
		progress = None
		use_progress = False
		on_convert_progress = None
		on_recognize_start = None
		on_recognize_progress = None
		if file_extension == 'pdf':
			conv = PDFConverter()
			use_progress = True
		elif file_extension == 'webp':
			conv = WebpConverter()
		elif file_extension == 'djvu':
			conv = DjVuConverter()
			use_progress = True
		elif OCRMultipageSourceFile.is_multipage_extension(file_extension):
			use_progress = True
		
		if use_progress:
			def on_cancel():
				if conv:
					conv.abort()
				ocr.abort()
			# Translators: Reporting when recognition (e.g. OCR) begins.
			progress = OCRProgressDialog(title=_N("Recognizing") + ' ' + os.path.basename(source_file), on_cancel=on_cancel)
			if conv:
				def on_convert_progress(conv, current, total):
					if current > 0:
						progress.tick(int(round(current / 2)), total, use_percentage=False)
			def on_recognize_progress(current, total):
				if current > 0:
					if conv:
						progress.tick(int(round((total + current) / 2)), total, use_percentage=False)
					else:
						progress.tick(current, total, use_percentage=False)
		else:
			# Translators: Reported when the recognition starts.
			speech.message(_("Process started"))
			self.beeper.start()
			def on_recognize_start(source_file):
				# Translators: Reporting when recognition (e.g. OCR) begins.
				speech.queue_message(_N("Recognizing"))
		
		def on_recognize_finish(source_file, result, arg=None):
			self.beeper.stop()
			if progress:
				progress.Close()
			if result and not isinstance(result, Exception):
				speech.cancel()
				OCRResultDialog(result=result)
		
		if not conv:
			ocr.recognize_files(source_file, [source_file], on_start=on_recognize_start, on_finish=on_recognize_finish, on_progress=on_recognize_progress, progress_timeout=self.progress_timeout)
			return True
		
		def on_convert_finish(success, converter):
			if success:
				ocr.recognize_files(converter.source_file, converter.results, on_start=on_recognize_start, on_finish=on_recognize_finish, on_finish_arg=conv, on_progress=on_recognize_progress, progress_timeout=self.progress_timeout)
			else:
				if progress:
					progress.Close()
				self.beeper.stop()
				def h():
					gui.mainFrame.prePopup()
					gui.messageBox(
						# Translators: Reported when unable to process a file for recognition.
						_("Error, the file could not be processed"),
						# Translators: The title of an error message dialog.
						_N("Error"),
						wx.OK | wx.ICON_ERROR)
					gui.mainFrame.postPopup()
				wx.CallAfter(h)
		
		conv.convert(source_file, on_convert_finish, on_convert_progress, self.progress_timeout)
		return True