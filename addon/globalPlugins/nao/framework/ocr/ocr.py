#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2023-10-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import api
import wx
import gui
import time
import queueHandler
from contentRecog import recogUi
from .uwp_ocr_service import UwpOCRService
from .. speech import speech
from .. generic import screen
from .. storage import storage_utils
from .. import language

language.initTranslation()

class OCRMultipageSourceFile:
	MULTIPAGE_FORMATS = ["gif", "tif", "tiff"]

	def is_multipage_format(filename):
		return OCRMultipageSourceFile.is_multipage_extension(storage_utils.file_extension(filename))

	def is_multipage_extension(file_extension):
		return file_extension and (file_extension.lower() in OCRMultipageSourceFile.MULTIPAGE_FORMATS)

	def __new__(cls, filename):
		if OCRMultipageSourceFile.is_multipage_format(filename):
			return super(OCRMultipageSourceFile, cls).__new__(cls)
		return None

	def __init__(self, filename):
		self.filename = filename
		self.remaining = self.page_count = wx.Image.GetImageCount(filename)

	def next(self):
		if self.remaining > 0:
			image = wx.Image(self.filename, index=self.page_count - self.remaining)
			self.remaining = self.remaining - 1
			if image:
				return wx.Bitmap(image, depth=24)
		return None

class OCR:
	def recognize_screenshot(on_start=None, on_finish=None, on_finish_arg=None, current_window=False):
		if isinstance(api.getFocusObject(), recogUi.RecogResultNVDAObject):
			# Translators: Reported when content recognition (e.g. OCR) is attempted,
			# but the user is already reading a content recognition result.
			speech.message(_N("Already in a content recognition result"))
			return False
		if not UwpOCRService.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			speech.message(_N("Windows OCR not available"))
			return False
		if screen.have_curtain():
			# Translators: Reported when screen curtain is enabled.
			speech.message(_N("Please disable screen curtain before using Windows OCR."))
			return False
		def failed(exception=None):
			# Translators: Reporting when recognition (e.g. OCR) fails.
			message = _N("Recognition failed")
			if exception:
				message += ': ' + str(exception)
			# Translators: The title of an error message dialog.
			wx.CallAfter(gui.messageBox, message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=gui.mainFrame)
			if on_finish:
				if on_finish_arg is None:
					on_finish(success=False)
				else:
					on_finish(success=False, arg=on_finish_arg)
		pixels, x, y, width, height = screen.take_snapshot_pixels(current_window=current_window)
		if not pixels:
			failed()
			return False
		def h(result):
			if not isinstance(result, Exception):
				try:
					resObj = recogUi.RecogResultNVDAObject(result=result.data)
					# This method queues an event to the main thread.
					resObj.setFocus()
				except Exception as e:
					result = e
			if isinstance(result, Exception):
				failed(result)
			elif on_finish:
				if on_finish_arg is None:
					on_finish(success=True)
				else:
					on_finish(success=True, arg=on_finish_arg)
		if on_start:
			on_start()
		UwpOCRService().push_pixels(pixels, width, height, h, x=x, y=y)
		return True

	def __init__(self):
		self.clear()

	def clear(self):
		self.service = None
		self.language = None
		self.source_file_list = []
		self.source_count = 0
		self.remaining = 0
		self.document_composer = None
		self.on_finish = None
		self.on_finish_arg = None
		self.on_progress = None
		self.progress_timeout = 1
		self.last_progress = 0
		self.must_abort = False

	def abort(self):
		self.must_abort = True

	def recognize_files(self, source_file, source_file_list, document_composer, language=None, on_start=None, on_finish=None, on_finish_arg=None, on_progress=None, progress_timeout=0):
		if not UwpOCRService.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			message = _N("Windows OCR not available")
			# Translators: The title of an error message dialog.
			wx.CallAfter(gui.messageBox, message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=gui.mainFrame)
			if on_finish:
				if on_finish_arg is None:
					on_finish(source_file=source_file, document=None)
				else:
					on_finish(source_file=source_file, document=None, arg=on_finish_arg)
			return
		self.clear()
		self.language = language
		self.document_composer = document_composer
		self.source_file_list = []
		self.source_count = 0
		self.on_finish = on_finish
		self.on_finish_arg = on_finish_arg
		self.on_progress = on_progress
		self.progress_timeout = progress_timeout
		self.last_progress = time.time()
		if on_start:
			on_start(source_file=source_file)
		for f in source_file_list:
			multi_page_file = OCRMultipageSourceFile(f)
			if (multi_page_file and multi_page_file.page_count > 1):
				self.source_file_list.append(multi_page_file)
				self.source_count = self.source_count + multi_page_file.page_count
			else:
				self.source_file_list.append(f)
				self.source_count = self.source_count + 1
		self.remaining = self.source_count
		if not self._recognize_next_page():
			if on_finish:
				if on_finish_arg is None:
					on_finish(source_file=source_file, document=None)
				else:
					on_finish(source_file=source_file, document=None, arg=on_finish_arg)
			self.clear()

	def _recognize_next_page(self):
		if self.must_abort: return False
		now = time.time()
		if now - self.last_progress >= self.progress_timeout:
			self.last_progress = now
			if self.on_progress:
				self.on_progress(self.source_count - self.remaining, self.source_count)
		if len(self.source_file_list) > 0:
			source = self.source_file_list[0]
			if isinstance(source, OCRMultipageSourceFile):
				bitmap = source.next()
				if source.remaining == 0:
					self.source_file_list.pop(0)
			else:
				bitmap = wx.Bitmap(source)
				self.source_file_list.pop(0)
			if bitmap:
				if not self.service:
					self.service = UwpOCRService()
				self.service.push_bitmap(bitmap, self._on_recognize_result, language=self.language)
				return True
		return False

	def _on_recognize_result(self, result):
		if not isinstance(result, Exception):
			try:
				self.document_composer.append_page(result)
			except Exception as e:
				result = e
		# This might get called from a background thread, so any UI calls must be queued to the main thread.
		if isinstance(result, Exception):
			# Translators: Reporting when recognition (e.g. OCR) fails.
			message = _N("Recognition failed")
			# Translators: The title of an error message dialog.
			wx.CallAfter(gui.messageBox, message + ': ' + str(result), _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=gui.mainFrame)
			if self.on_finish:
				if self.on_finish_arg is None:
					self.on_finish(source_file=self.document_composer.Document.SourceFile, document=result)
				else:
					self.on_finish(source_file=self.document_composer.Document.SourceFile, document=result, arg=self.on_finish_arg)
			self.clear()
			return
		
		self.remaining = self.remaining - 1
		if not self._recognize_next_page():
			# No more pages
			def h():
				if self.on_finish:
					if self.must_abort:
						if self.on_finish_arg is None:
							self.on_finish(source_file=self.document_composer.Document.SourceFile, document=None)
						else:
							self.on_finish(source_file=self.document_composer.Document.SourceFile, document=None, arg=self.on_finish_arg)
					else:
						self.document_composer.end()
						if self.on_finish_arg is None:
							self.on_finish(source_file=self.document_composer.Document.SourceFile, document=self.document_composer.Document)
						else:
							self.on_finish(source_file=self.document_composer.Document.SourceFile, document=self.document_composer.Document, arg=self.on_finish_arg)
				self.clear()
			queueHandler.queueFunction(queueHandler.eventQueue, h)