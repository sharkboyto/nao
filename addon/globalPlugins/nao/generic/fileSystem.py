#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-16
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import api
import ui
import os
import addonHandler
from .xplorer2Helper import Xplorer2Helper
from .totalCommanderHelper import TotalCommanderHelper
from comtypes.client import CreateObject as COMCreate

addonHandler.initTranslation()

_shell = None

def get_selected_file(): #For this method thanks to some nvda addon developers ( code snippets and suggestion)
	file_path = False
	# We check if we are in the xplorer2
	xplorer2 = Xplorer2Helper()
	if xplorer2.is_valid():
		file_path = xplorer2.currentFileWithPath()
	else:
		# We check if we are in the Total Commander
		total_commander = TotalCommanderHelper()
		if total_commander.is_valid():
			file_path = total_commander.currentFileWithPath()
		else:
			# We check if we are in the Windows Explorer.
			fg = api.getForegroundObject()
			if (fg.role != api.controlTypes.Role.PANE and fg.role != api.controlTypes.Role.WINDOW) or fg.appModule.appName != "explorer":
				ui.message(_("You must be in a Windows File Explorer window"))
			else:
				global _shell
				if not _shell:
					_shell = COMCreate("shell.application")
				# We go through the list of open Windows Explorers to find the one that has the focus.
				for window in _shell.Windows():
					if window.hwnd == fg.windowHandle:
						# Now that we have the current folder, we can explore the SelectedItems collection.
						file_path = str(window.Document.FocusedItem.path)
						break
				else: # loop exhausted
					desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
					file_path = desktop_path + '\\' + api.getDesktopObject().objectWithFocus().name
	return file_path
