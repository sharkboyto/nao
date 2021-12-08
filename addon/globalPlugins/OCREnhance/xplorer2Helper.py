#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-08
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import ctypes
import api
from .totalCommanderHelper import get_window_text

class Xplorer2Helper:
	def __init__(self):
		self.handle = None
		fg = api.getForegroundObject()
		if fg and fg.appModule and fg.appModule.appName and fg.appModule.appName.startswith('xplorer2'):
			self.handle = ctypes.windll.user32.GetForegroundWindow()
			if self.handle and not self.currentFolderHandle():
				self.handle = None

	def is_valid(self):
		return self.handle != None

	def is_active(self):
		return self.handle and self.handle == ctypes.windll.user32.GetForegroundWindow()

	def currentFolderHandle(self):
		handle = ctypes.windll.user32.GetDlgItem(self.handle, 59392) #ReBarWindow32
		if handle:
			handle = ctypes.windll.user32.GetDlgItem(handle, 60160) #AddressBar
		if handle:
			handle = ctypes.windll.user32.GetDlgItem(handle, 1500) #ComboBox
		return handle

	def currentFolder(self):
		handle = self.currentFolderHandle()
		if handle:
			return get_window_text(handle)
		return False

	def currentFile(self):
		file = ""
		if self.is_active():
			obj = api.getFocusObject()
			if obj and obj.name:
				file = obj.name.split("\t")[0]
				if file == '..':
					file = ""
		return file

	def currentFileWithPath(self):
		file = self.currentFile()
		if file:
			file = self.currentFolder() + "\\" + file
		return file
