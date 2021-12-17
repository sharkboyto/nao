#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# 2021-12-08, added script decorator and category for two main keys.
# 2021-12-11, fixed file extension check.
# 2021-12-14, xplorer2 support
# 2021-12-15, new result dialog
# 2021-12-16, code refactoring
#Last update 2021-12-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import globalPluginHandler
import addonHandler
from scriptHandler import script

from .framework import *
begin_framework_imports()
from framework.speech import speech
from framework.generic import fileSystem
from framework.generic.beepThread import BeepThread
from framework.ocr.recogUiEnhance import RecogUiEnhance
from framework.ocr.recogUiEnhanceResult import RecogUiEnhanceResultDialog
from framework.converters.pdf_converter import PDFConverter
from framework.converters.webp_converter import WebpConverter
end_framework_imports()

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = ADDON_SUMMARY
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.supported_extensions = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp"]
		self.beeper = BeepThread()
		PDFConverter().clear_all()
		WebpConverter().clear_all()

	@script(
		# Translators: Message presented in input help mode.
		description=_("Take a full screen shot and recognize it."),
		gesture="kb:NVDA+shift+control+R"
	)
	def script_doRecognizeScreenshotObject(self, gesture):
		RecogUiEnhance.recognize_screenshot()

	@script(
		# Translators: Message presented in input help mode.
		description=_("Recognize the content of the selected image or PDF file."),
		gesture="kb:NVDA+shift+r"
	)
	def script_doRecognizeFileObject(self, gesture):
		self.recognize_file(fileSystem.get_selected_file())

	def recognize_file(self, source_file):
		if not source_file:
			return False
		if not RecogUiEnhance.is_uwp_ocr_available():
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
			RecogUiEnhanceResultDialog(source_file=source_file, result=result, pages_offset=pages_offset)
		
		speech.message(_("Process started"))
		self.beeper.start()
		if file_extension == 'pdf':
			conv = PDFConverter()
		elif file_extension == 'webp':
			conv = WebpConverter()
		else:
			RecogUiEnhance().recognize_files(source_file, [source_file], recognize_finish)
			return True
		def on_convert(success, converter):
			if success:
				RecogUiEnhance().recognize_files(converter.source_file, converter.results, recognize_finish, conv)
			else:
				speech.queue_message(_("Error, the file could not be processed."))
				self.beeper.stop()
		conv.to_png(source_file, on_convert)
		return True