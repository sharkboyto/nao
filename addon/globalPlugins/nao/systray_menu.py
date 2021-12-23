#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-23
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import gui
import wx
import addonHandler

from . import donate
from .framework import language

language.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

class SysTrayMenu:
	def __init__(self):
		self._menu = None
		self._donate = None
		self._tool_menu_root = None

	def create(self):
		if not self._tool_menu_root:
			self._menu = wx.Menu()
			tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			# Translators: The label of the button to donate
			self._donate = self._menu.Append(wx.ID_ANY, _N("&Donate"), _N("Please Donate"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: donate.open(), self._donate)
			self._tool_menu_root = tools_menu.AppendSubMenu(self._menu, ADDON_SUMMARY, ADDON_SUMMARY)

	def destroy(self):
		try:
			gui.mainFrame.sysTrayIcon.toolsMenu.Remove(self._tool_menu_root)
		except Exception:
			pass
		self._menu = None
		self._donate = None
		self._tool_menu_root = None
