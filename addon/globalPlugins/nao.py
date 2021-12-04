#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-11-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import globalPluginHandler
import os
import ui
import winVersion
import vision
import api
import threading
import subprocess
import nvwave
import speech
import addonHandler
from comtypes.client import CreateObject as COMCreate
from .OCREnhance import recogUiEnhance, beepThread, totalCommanderHelper
from .OCREnhance.recogUiEnhance import queue_ui_message
from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
from contentRecog import recogUi

addonHandler.initTranslation()

# Global variables
filePath = ""
fileExtension = ""
fileName = ""
suppFiles = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp"]
addonPath = os.path.dirname(__file__)
pdfToPngToolPath = "\""+os.path.join (addonPath, "tools", "pdftopng.exe")+"\""
pdfToImagePath = "" + os.path.join (addonPath, "images") + ""
pdfToImageFileNamePath = pdfToImagePath + "\\img"

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.recogUiEnhance = recogUiEnhance.RecogUiEnhance()
		self.beeper = beepThread.BeepThread()

	def script_doRecognizeScreenshotObject(self, gesture):
		if not winVersion.isUwpOcrAvailable():
			# Translators: Reported when Windows OCR is not available.
			ui.message(_("Windows OCR not available"))
			return
		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
		isScreenCurtainRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
		if isScreenCurtainRunning:
			# Translators: Reported when screen curtain is enabled.
			ui.message(_("Please disable screen curtain before using Windows OCR."))
			return
		self.recogUiEnhance.recognizeScreenshotObject()

	def script_doRecognizeFileObject(self, gesture):
		if not winVersion.isUwpOcrAvailable():
			# Translators: Reported when Windows OCR is not available.
			ui.message(_("Windows OCR not available"))
			return
			
		p = self.getFilePath()
		if p == True:
			if fileExtension == 'pdf':
				self.convertPdfToPng()
			else:
				ui.message(_("Process started"))
				self.recogUiEnhance.recognizeImageFileObject(filePath)
		else:
			pass

	def getFilePath(self): #For this method thanks to some nvda addon developers ( code snippets and suggestion)
		global filePath
		global fileExtension
		global fileName
		
		# We check if we are in the Total Commander
		tcmd = totalCommanderHelper.TotalCommanderHelper()
		if tcmd.is_valid():
			filePath = tcmd.currentFileWithPath()
			if not filePath:
				return False
		else:
			# We check if we are in the Windows Explorer.
		fg = api.getForegroundObject()
			if (fg.role != api.controlTypes.Role.PANE and fg.role != api.controlTypes.Role.WINDOW) or fg.appModule.appName != "explorer":
			ui.message(_("You must be in a Windows File Explorer window"))
				return False
		
		self.shell = COMCreate("shell.application")
		desktop = False
		# We go through the list of open Windows Explorers to find the one that has the focus.
		for window in self.shell.Windows():
			if window.hwnd == fg.windowHandle:
				focusedItem=window.Document.FocusedItem
				break
		else: # loop exhausted
			desktop = True
		# Now that we have the current folder, we can explore the SelectedItems collection.
		if desktop:
			desktopPath = desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
			fileName = api.getDesktopObject().objectWithFocus().name
			filePath = desktopPath + '\\' + fileName
		else:
			filePath = str(focusedItem.path)
			fileName = str(focusedItem.name)
		
		# Getting the extension to check if is a supported file type.
		fileExtension = filePath[-5:].lower() # Returns .jpeg or x.pdf
		if fileExtension.startswith("."): # Case of a  .jpeg file
			fileExtension = fileExtension[1:] # just jpeg
		else:
			fileExtension = fileExtension[2:] # just pdf
		if fileExtension in suppFiles:
			return True # Is a supported file format, so we can make OCR
		else:
			ui.message(_("File not supported"))
			return False # It is a file format not supported so end the process.

	def convertPdfToPng(self):
		if isinstance(api.getFocusObject(), recogUi.RecogResultNVDAObject):
			# Translators: Reported when content recognition (e.g. OCR) is attempted,
			# but the user is already reading a content recognition result.
			ui.message(_("Already in a content recognition result"))
			return
		
		self._thread = threading.Thread(target = self._pdfToPngThread)
		self._thread.setDaemon(True)
		self._thread.start()

	def _pdfToPngThread(self):
		# The next two lines are to prevent the cmd from being displayed.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		try:
			for f in os.listdir(pdfToImagePath):
				os.remove(os.path.join(pdfToImagePath, f))
		except FileNotFoundError:
			queue_ui_message(_("Error, file not found"))
			pass
		command = "{} \"{}\" \"{}\"".format(pdfToPngToolPath, filePath, pdfToImageFileNamePath)
		
		queue_ui_message(_("Process started"))
		self.beeper.start()
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		
		if p.returncode == 0:
			self.recogUiEnhance.recognizePdfFileObject(os.listdir(pdfToImagePath), pdfToImagePath, self._pdfToPngFinish)
		else:
			queue_ui_message(_("Error, the file could not be processed."))
			self.beeper.stop()

	def _pdfToPngFinish(self):
		self.beeper.stop()
		speech.cancelSpeech()
		try:
			for f in os.listdir(pdfToImagePath):
				os.remove(os.path.join(pdfToImagePath, f))
		except FileNotFoundError:
			pass

	__gestures={
		"kb:NVDA+shift+control+R": "doRecognizeScreenshotObject",
		"kb:NVDA+shift+R": "doRecognizeFileObject"
	}