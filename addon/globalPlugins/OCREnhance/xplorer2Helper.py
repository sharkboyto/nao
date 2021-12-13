#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-13
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import ctypes
import api
from .totalCommanderHelper import get_window_text
from .user32Menu import User32Menu
import time
import threading
import re

class Xplorer2Helper:
	def __init__(self):
		self.handle = None
		self._thread_context_menu = None
		fg = api.getForegroundObject()
		if fg and fg.appModule and fg.appModule.appName and fg.appModule.appName.startswith('xplorer2'):
			self.handle = ctypes.windll.user32.GetForegroundWindow()
			if self.handle:
				self._thread_event = threading.Event()

	def is_valid(self):
		return self.handle != None

	def is_active(self):
		return self.handle and self.handle == ctypes.windll.user32.GetForegroundWindow()

	def currentFolderHandle(self):
		handle_ret = None
		if self.handle:
			handle = ctypes.windll.user32.GetDlgItem(self.handle, 59392) #ReBarWindow32
			if handle and ctypes.windll.user32.IsWindowVisible(handle):
				handle = ctypes.windll.user32.GetDlgItem(handle, 60160) #AddressBar
			if handle and ctypes.windll.user32.IsWindowVisible(handle):
				handle_ret = ctypes.windll.user32.GetDlgItem(handle, 1500) #ComboBox
		return handle_ret

	def currentFolder(self):
		handle = self.currentFolderHandle()
		if handle:
			return get_window_text(handle)
		elif self.handle:
			# we try to catch the folder from the right-click context menu
			if self._thread_context_menu:
				self._thread_context_menu = None
				self._thread_event.wait(timeout=2)
			
			self._folder = None
			self._thread_context_menu = threading.Thread(target = self._wait_context_menu)
			self._thread_context_menu.setDaemon(True)
			self._thread_context_menu.start()
			
			# open the context menu
			if ctypes.windll.user32.SendMessageW(self.handle, 0x111, 0x80B1, 0) == 0:
				self._thread_event.wait(timeout=2)
			else:
				self._thread_context_menu = None
			
			if self._folder:
				return self._folder
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

	def _wait_context_menu(self):
		# wait the context menu and catch it
		while self._thread_context_menu:
			time.sleep(0.1)
			menu = User32Menu.get_context_menu()
			if menu:
				self._thread_context_menu = None
				for item in menu.items:
					# the current folder is the default item
					if (item.text and item.is_default):
						self._folder = re.sub('^[\d]*\s', r'', item.text) # remove index number
						break
				#we can close the context menu
				ctypes.windll.user32.SendMessageW(menu.hwnd, 0x10, 0, 0) # WM_CLOSE
		self._thread_event.set()

	def currentFileWithPath(self):
		file = self.currentFile()
		folder = self.currentFolder()
		if file and folder:
			return folder + "\\" + file
		return None
