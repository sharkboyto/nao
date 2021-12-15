#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-15
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import api
import os
import ui
import winGDI
import screenBitmap
import wx
import queueHandler
from contentRecog import uwpOcr, recogUi, LinesWordsResult
from .recogUiEnhanceResult import RecogUiEnhanceResultDialog, RecogUiEnhanceResultPageOffset
import addonHandler

def queue_ui_message(message):
	queueHandler.queueFunction(queueHandler.eventQueue, ui.message, message)

addonHandler.initTranslation()

class RecogUiEnhance:
	def __init__(self):
		self.bmp_list = []
		self.results = []
		self.pages_offset = []
		self.on_finish = None

	def recognizeImageFileObject(self, filePath):
		recognizer = uwpOcr.UwpOcr()
		try:
			imgPath = os.path.abspath(filePath)
			bmp =  wx.Bitmap(imgPath)
			width, height = bmp.Size.Get()
			imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
		except ValueError:
			ui.message(_("Internal conversion error"))
			return
		if recogUi._activeRecog:
			recogUi._activeRecog.cancel()
			recogUi._activeRecog = None
		self.file_name = filePath
		self.results = []
		self.pages_offset = []
		ui.message(_("Recognizing"))
		pixels = (winGDI.RGBQUAD*bmp.GetWidth()*bmp.GetHeight())()
		bmp.CopyToBuffer(pixels, format=wx.BitmapBufferFormat_ARGB32)
		recogUi._activeRecog = recognizer
		recognizer.recognize(pixels, imgInfo, self._FileRecogOnResult)
		
	def _FileRecogOnResult(self, result):
		recogUi._activeRecog = None
		# This might get called from a background thread, so any UI calls must be queued to the main thread.
		if isinstance(result, Exception):
			# Translators: Reported when recognition (e.g. OCR) fails.
			log.error("Recognition failed: %s" % result)
			queue_ui_message(_("Recognition failed"))
			self.results = []
			self.pages_offset = []
			return
		
		if len(self.pages_offset) == 0:
			self.pages_offset.append(RecogUiEnhanceResultPageOffset(0, result.textLen))
		else:
			self.pages_offset.append(RecogUiEnhanceResultPageOffset(self.pages_offset[len(self.pages_offset) - 1].end, result.textLen))
		
		# Result is a LinesWordsResult, we store all pages data objects that we will merge later in a single LinesWordsResult
		for line in result.data:
			self.results.append(line)
		
		queueHandler.queueFunction(queueHandler.eventQueue, self._showResult, result.imageInfo)

	def recognizeScreenshotObject(self):
		if isinstance(api.getFocusObject(), recogUi.RecogResultNVDAObject):
			# Translators: Reported when content recognition (e.g. OCR) is attempted,
			# but the user is already reading a content recognition result.
			ui.message(_("Already in a content recognition result"))
			return
		recognizer = uwpOcr.UwpOcr()
		try:
			s = wx.ScreenDC()
			width, height = s.Size.Get()
			imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
		except ValueError:
			ui.message(_("Internal conversion error"))
			return
		if recogUi._activeRecog:
			recogUi._activeRecog.cancel()
			recogUi._activeRecog = None
		ui.message(_("Recognizing"))
		sb = screenBitmap.ScreenBitmap(imgInfo.recogWidth, imgInfo.recogHeight)
		pixels = sb.captureImage(0, 0, width, height)
		recogUi._activeRecog = recognizer
		recognizer.recognize(pixels, imgInfo, recogUi._recogOnResult)

	def recognizePdfFileObject(self, file_name, filePathList, pdfToImagePath, onFinish = None):
		if recogUi._activeRecog:
			recogUi._activeRecog.cancel()
			recogUi._activeRecog = None
		self.file_name = file_name
		self.bmp_list = []
		self.results = []
		self.pages_offset = []
		self.on_finish = onFinish
		queue_ui_message(_("Recognizing"))
		for f in filePathList:
			bmp =  wx.Bitmap(str(os.path.join(pdfToImagePath, f)))
			self.bmp_list.append(bmp)
		self._recognize_next_pdf_page()

	def _recognize_next_pdf_page(self):
		if len(self.bmp_list) > 0:
			recognizer = uwpOcr.UwpOcr()
			bmp = self.bmp_list.pop(0)
			width, height = bmp.Size.Get()
			imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
			pixels = (winGDI.RGBQUAD*width*height)()
			bmp.CopyToBuffer(pixels, format=wx.BitmapBufferFormat_ARGB32)
			recogUi._activeRecog = recognizer
			recognizer.recognize(pixels, imgInfo, self._PdfRecogOnResult)
			return True
		if self.on_finish:
			self.on_finish()
			self.on_finish = None
		return False

	def _PdfRecogOnResult(self, result):
		recogUi._activeRecog = None
		# This might get called from a background thread, so any UI calls must be queued to the main thread.
		if isinstance(result, Exception):
			# Translators: Reported when recognition (e.g. OCR) fails.
			log.error("Recognition failed: %s" % result)
			queue_ui_message(_("Recognition failed"))
			self.bmp_list = []
			self.results = []
			self.pages_offset = []
			if self.on_finish:
				self.on_finish()
				self.on_finish = None
			return
		
		if len(self.pages_offset) == 0:
			self.pages_offset.append(RecogUiEnhanceResultPageOffset(0, result.textLen))
		else:
			self.pages_offset.append(RecogUiEnhanceResultPageOffset(self.pages_offset[len(self.pages_offset) - 1].end, result.textLen))
		
		# Result is a LinesWordsResult, we store all pages data objects that we will merge later in a single LinesWordsResult
		for line in result.data:
			self.results.append(line)
		
		if not self._recognize_next_pdf_page():
			# No more pages
			queueHandler.queueFunction(queueHandler.eventQueue, self._showResult, result.imageInfo)

	def _showResult(self, imageInfo):
		result = LinesWordsResult(self.results, imageInfo)
		dlg = RecogUiEnhanceResultDialog(file_name=self.file_name,result=result,pages_offset=self.pages_offset)
		self.results = []
		self.pages_offset = []
