#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-31
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import gui
import wx
import addonHandler

from . import donate
from .framework import language

language.initTranslation()

class SysTrayMenu:
	def __init__(self):
		self._tool_menu_root = None

	def create(self, on_updates_check=None):
		if not self._tool_menu_root:
			_menu = wx.Menu()
			tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			# Translators: The label of the button to donate
			_donate = _menu.Append(wx.ID_ANY, _N("&Donate"), _N("Please Donate"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: donate.open(), _donate)
			if on_updates_check:
				# Translators: The label of a menu item to manually check for an updated version of NAO
				_check_updates = _menu.Append(wx.ID_ANY, _N("&Check for update..."))
				gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: on_updates_check(), _check_updates)
			summary = addonHandler.getCodeAddon().manifest["summary"]
			self._tool_menu_root = tools_menu.AppendSubMenu(_menu, summary, summary)

	def terminate(self):
		if self._tool_menu_root:
			try:
				gui.mainFrame.sysTrayIcon.toolsMenu.Remove(self._tool_menu_root)
			except Exception:
				pass
			self._tool_menu_root = None
