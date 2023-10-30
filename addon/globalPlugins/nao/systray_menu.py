#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-04-23
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import gui
from .framework import language

language.initTranslation()

class SysTrayMenu:
	def __init__(self):
		self._tool_menu_root = None
		self._terminate_handler = None

	def create(self, on_updates_check=None, on_select_file=None):
		if not self._tool_menu_root:
			import wx
			import addonHandler
			import webbrowser
			from . import donate
			from .nao_document_cache import NaoDocumentCache
			from .framework.threading import ProgramTerminateHandler
			
			_menu = wx.Menu()
			tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			
			if on_select_file:
				# Translators: The label of the button to select a file
				_browse = _menu.Append(wx.ID_ANY, _N("file chooser"))
				gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: on_select_file(), _browse)
			
			# Translators: The label of the button to donate
			_donate = _menu.Append(wx.ID_ANY, _N("&Donate"), _N("Please Donate"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: donate.open(), _donate)
			
			# Translators: A label for a shortcut to go to NAO website
			_website = _menu.Append(wx.ID_ANY, _("NAO web site"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: webbrowser.open("https://nvda-nao.org"), _website)
			
			_git = _menu.Append(wx.ID_ANY, "Git")
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: webbrowser.open("https://nvda-nao.org/git"), _git)
			
			if on_updates_check:
				# Translators: The label of a menu item to manually check for an updated version of NAO
				_check_updates = _menu.Append(wx.ID_ANY, _N("&Check for update..."))
				gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: on_updates_check(), _check_updates)
					
			# Translators: The label of a menu item to clear the cache
			_clear_cache = _menu.Append(wx.ID_ANY, _("Clear cache"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: NaoDocumentCache.clear(), _clear_cache)
			
			summary = addonHandler.getCodeAddon().manifest["summary"]
			self._tool_menu_root = tools_menu.AppendSubMenu(_menu, summary, summary)
			self._terminate_handler = ProgramTerminateHandler(self.destroy)

	def destroy(self):
		if self._tool_menu_root:
			self._terminate_handler.unregister()
			try:
				gui.mainFrame.sysTrayIcon.toolsMenu.Remove(self._tool_menu_root)
			except Exception:
				pass
			self._tool_menu_root = None
			self._terminate_handler = None