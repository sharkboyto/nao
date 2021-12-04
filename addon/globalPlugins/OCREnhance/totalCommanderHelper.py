#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-11-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import winUser
import ctypes
import api
from appModules.totalcmd import AppModule as TotalCommanderAppModule

def get_window_text(handle):
	if handle:
		# WM_GETTEXTLENGTH
		length = ctypes.windll.user32.SendMessageW(handle, 14, 0, 0)
		if length > 0:
			length = (length + 1) * 2
			text = ctypes.create_string_buffer(length)
			# WM_GETTEXT
			ctypes.windll.user32.SendMessageW(handle, 13, length, ctypes.addressof(text))
			return text.raw.decode('utf16')[:-1]
	return ""

class TotalCommanderHelper:
	def __init__(self):
		self.handle = None
		fg = api.getForegroundObject()
		if fg and isinstance(fg.appModule, TotalCommanderAppModule):
			self.handle = ctypes.windll.user32.GetForegroundWindow()
			if self.handle and self.currentPanel() <= 0:
				self.handle = None

	def is_valid(self):
		return self.handle != None

	def is_active(self):
		return self.handle and self.handle == ctypes.windll.user32.GetForegroundWindow()

	def sendMessage(self, param1, param2):
		if self.handle:
			return ctypes.windll.user32.SendMessageW(self.handle, 1074, param1, param2)
		return False

	def currentPanel(self):
		return self.sendMessage(1000, 0)

	def currentFolder(self):
		folder = get_window_text(self.sendMessage(21, 0))
		if folder and folder.endswith('>'):
			folder = folder[:-1]
		return folder

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
