#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import api
import winGDI
import wx
import queueHandler
import addonHandler
import winVersion
from contentRecog import uwpOcr, recogUi, LinesWordsResult
from .. speech import speech
from .. generic import screen

addonHandler.initTranslation()

class OCRResultPageOffset():
	def __init__(self, start, length):
		self.start = start
		self.end = start + length

class OCR:
	def is_uwp_ocr_available():
		return winVersion.isUwpOcrAvailable()

	def recognize_screenshot(on_finish=None, on_finish_arg=None):
		if isinstance(api.getFocusObject(), recogUi.RecogResultNVDAObject):
			# Translators: Reported when content recognition (e.g. OCR) is attempted,
			# but the user is already reading a content recognition result.
			speech.message(_("Already in a content recognition result"))
			return
		if not OCR.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.message(_("Windows OCR not available"))
			return
		if screen.have_curtain():
			# Translators: Reported when screen curtain is enabled.
			speech.message(_("Please disable screen curtain before using Windows OCR."))
			return
		speech.message(_("Recognizing"))
		pixels, width, height = screen.take_snapshot_pixels()
		recognizer = uwpOcr.UwpOcr()
		try:
			imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
		except ValueError:
			speech.message(_("Internal conversion error"))
			return
		if recogUi._activeRecog:
			recogUi._activeRecog.cancel()
			recogUi._activeRecog = None
		recogUi._activeRecog = recognizer
		def h(result):
			recogUi._recogOnResult(result)
			recogUi._activeRecog = None
			if on_finish:
				if on_finish_arg is None:
					on_finish()
				else:
					on_finish(arg=on_finish_arg)
		recognizer.recognize(pixels, imgInfo, h)

	def __init__(self):
		self.clear()

	def clear(self):
		self.bmp_list = []
		self.results = []
		self.pages_offset = []
		self.on_finish = None
		self.on_finish_arg = None
		self.source_file = None

	def recognize_files(self, source_file, source_file_list, on_finish=None, on_finish_arg=None):
		if not OCR.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.queue_message(_("Windows OCR not available"))
			if on_finish:
				if on_finish_arg is None:
					on_finish(source_file=source_file, result=None, pages_offset=None)
				else:
					on_finish(source_file=source_file, result=None, pages_offset=None, arg=on_finish_arg)
			return
		if recogUi._activeRecog:
			recogUi._activeRecog.cancel()
			recogUi._activeRecog = None
		self.clear()
		self.source_file = source_file
		self.on_finish = on_finish
		self.on_finish_arg = on_finish_arg
		speech.queue_message(_("Recognizing"))
		for f in source_file_list:
			bmp = wx.Bitmap(f)
			self.bmp_list.append(bmp)
		self._recognize_next_page()

	def _recognize_next_page(self):
		if len(self.bmp_list) > 0:
			recognizer = uwpOcr.UwpOcr()
			bmp = self.bmp_list.pop(0)
			width, height = bmp.Size.Get()
			imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
			pixels = (winGDI.RGBQUAD*width*height)()
			bmp.CopyToBuffer(pixels, format=wx.BitmapBufferFormat_ARGB32)
			recogUi._activeRecog = recognizer
			recognizer.recognize(pixels, imgInfo, self._on_recognize_result)
			return True
		return False

	def _on_recognize_result(self, result):
		recogUi._activeRecog = None
		# This might get called from a background thread, so any UI calls must be queued to the main thread.
		if isinstance(result, Exception):
			# Translators: Reported when recognition (e.g. OCR) fails.
			log.error("Recognition failed: %s" % result)
			speech.queue_message(_("Recognition failed"))
			if self.on_finish:
				if self.on_finish_arg is None:
					self.on_finish(source_file=self.source_file, result=None, pages_offset=None)
				else:
					self.on_finish(source_file=self.source_file, result=None, pages_offset=None, arg=self.on_finish_arg)
			self.clear()
			return
		
		if len(self.pages_offset) == 0:
			self.pages_offset.append(OCRResultPageOffset(0, result.textLen))
		else:
			self.pages_offset.append(OCRResultPageOffset(self.pages_offset[len(self.pages_offset) - 1].end, result.textLen))
		
		# Result is a LinesWordsResult, we store all pages data objects that we will merge later in a single LinesWordsResult
		for line in result.data:
			self.results.append(line)
		
		if not self._recognize_next_page():
			# No more pages
			def h():
				if self.on_finish:
					if self.on_finish_arg is None:
						self.on_finish(source_file=self.source_file, result=LinesWordsResult(self.results, result.imageInfo), pages_offset=self.pages_offset)
					else:
						self.on_finish(source_file=self.source_file, result=LinesWordsResult(self.results, result.imageInfo), pages_offset=self.pages_offset, arg=self.on_finish_arg)
				self.clear()
			queueHandler.queueFunction(queueHandler.eventQueue, h)