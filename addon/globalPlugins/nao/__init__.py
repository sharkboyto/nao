#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-02-04
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import globalPluginHandler
import addonHandler
from scriptHandler import script
from baseObject import ScriptableObject
import globalVars

from .nao_document_cache import NaoDocumentCache
from .framework.ocr.ocr_helper import OCRHelper
from .framework.storage import explorer
from .framework.threading import ProgramTerminate
from .framework import language

language.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
UPDATES_URL = "https://nvda-nao.org/updates"
OCR_DOCUMENT_FILE_EXTENSION = "nao-document"

def BrowseAndRecognize():
	import gui
	import wx
	def h():
		# Translators: The title of a select file dialog
		with wx.FileDialog(gui.mainFrame, _N("file chooser"), style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
			if file_dialog.ShowModal() != wx.ID_CANCEL:
				filename = file_dialog.GetPath()
				OCRHelper(ocr_document_file_extension=OCR_DOCUMENT_FILE_EXTENSION, ocr_document_file_cache=NaoDocumentCache(), speak_errors=False).recognize_file(filename)
	wx.CallAfter(h)

class RecognizableFileObject(ScriptableObject):
	# Allow the bound gestures to be edited through the Input Gestures dialog (see L{gui.prePopup})
	isPrevFocusOnNvdaPopup = True

	@script(
		# Translators: Message presented in input help mode.
		description=_("Recognizes the content of the selected image or PDF file"),
		gesture="kb:NVDA+shift+R",
		category=ADDON_SUMMARY
	)
	def script_recognize_file(self, gesture):
		try:
			filename = explorer.get_selected_file()
		except:
			filename = None
		if filename:
			OCRHelper(ocr_document_file_extension=OCR_DOCUMENT_FILE_EXTENSION, ocr_document_file_cache=NaoDocumentCache()).recognize_file(filename)
		else:
			BrowseAndRecognize()

def disableInSecure(cls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return cls

@disableInSecure
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		from .nao_pickle import NaoPickle
		from .systray_menu import SysTrayMenu
		from .framework.generic.updates import AutoUpdates, ManualUpdatesCheck
		super(GlobalPlugin, self).__init__()
		self._systray = SysTrayMenu()
		self._systray.create(on_updates_check=lambda: ManualUpdatesCheck(UPDATES_URL, pickle=NaoPickle()), on_select_file=BrowseAndRecognize)
		self._auto_updates = AutoUpdates(url=UPDATES_URL, pickle=NaoPickle())
		self._scheduled_cache_purge = NaoDocumentCache.schedule_purge()

	def terminate(self):
		ProgramTerminate()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj:
			if explorer.is_explorer(obj):
				clsList.insert(0, RecognizableFileObject)
			elif explorer.is_totalcommander(obj):
				clsList.insert(0, RecognizableFileObject)
			elif explorer.is_xplorer2(obj):
				clsList.insert(0, RecognizableFileObject)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Take a full screen shot and recognize it"),
		gesture="kb:NVDA+shift+control+R",
		category=ADDON_SUMMARY
	)
	def script_recognize_screenshot(self, gesture):
		OCRHelper.recognize_screenshot()