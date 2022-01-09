#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-09
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import globalPluginHandler
import addonHandler
from scriptHandler import script
from baseObject import ScriptableObject

from .systray_menu import SysTrayMenu
from .nao_pickle import NaoPickle

from .framework.generic.updates import AutoUpdates, ManualUpdatesCheck
from .framework.ocr.ocr_helper import OCRHelper
from .framework.generic import fileSystem
from .framework import language

language.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
UPDATES_URL = "https://nvda-nao.org/updates"
OCR_RESULT_FILE_EXTENSION = "nao_result"

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
		OCRHelper(ocr_result_file_extension=OCR_RESULT_FILE_EXTENSION).recognize_file(fileSystem.get_selected_file())

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._systray = SysTrayMenu()
		self._systray.create(on_updates_check=lambda: ManualUpdatesCheck(UPDATES_URL, pickle=NaoPickle()))
		self._auto_updates = AutoUpdates(UPDATES_URL, NaoPickle())

	def terminate(self):
		self._systray.terminate()
		self._auto_updates.terminate()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj:
			if fileSystem.is_explorer(obj):
				clsList.insert(0, RecognizableFileObject)
			elif fileSystem.is_totalcommander(obj):
				clsList.insert(0, RecognizableFileObject)
			elif fileSystem.is_xplorer2(obj):
				clsList.insert(0, RecognizableFileObject)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Take a full screen shot and recognize it"),
		gesture="kb:NVDA+shift+control+R",
		category=ADDON_SUMMARY
	)
	def script_recognize_screenshot(self, gesture):
		OCRHelper.recognize_screenshot()