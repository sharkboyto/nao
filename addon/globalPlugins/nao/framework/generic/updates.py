#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import json
import threading
import time
import os
import wx
import gui
import winsound
import globalVars
import tempfile
import stat
import addonHandler
import queueHandler
from gui import addonGui

from . import version
from . import window
from .http import json_post
from .. import language

language.initTranslation()

CHECK_INTERVAL = 86400 # 1 day
CHECK_INTERVAL_FAIL = 10800 # 3 hours

class UpdatesConfirmDialog(wx.Dialog):
	def __init__(self, parent, on_accept, on_cancel, version='', title=None, message=None):
		name = addonHandler.getCodeAddon().manifest["summary"]
		if not title:
			# Translators: The title of the update dialog
			title = _("{name} Update")
			title = title.format(name=name)
		if not message:
			if not version: version=''
			# Translators: The version in the message of the update dialog
			message = name + ' ' + _N("Version") + ' ' + version
			# Translators: The message of the update dialog
			message = message + ' ' + _("is available")
			# Translators: The message of the update dialog
			message = message + ' \n' + _("Do you want to download and install it?")
		
		super(UpdatesConfirmDialog, self).__init__(parent, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		
		sHelper.addItem(wx.StaticText(self, label=message))
		bHelper = sHelper.addDialogDismissButtons(gui.guiHelper.ButtonHelper(wx.HORIZONTAL))
		
		def _on_accept(evt):
			self.Destroy()
			if on_accept: on_accept()
		
		def _on_cancel(evt):
			self.Destroy()
			if on_cancel: on_cancel()
		
		confirmButton = bHelper.addButton(self, id=wx.ID_YES)
		cancelButton = bHelper.addButton(self, id=wx.ID_NO)
		cancelButton.Bind(wx.EVT_BUTTON, _on_cancel)
		
		self.Bind(wx.EVT_CLOSE, _on_cancel)
		
		confirmButton.SetDefault()
		confirmButton.Bind(wx.EVT_BUTTON, _on_accept)
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Center(wx.BOTH|wx.Center)

	def Ask(on_accept, on_cancel, version='', title=None, message=None):
		def h():
			gui.mainFrame.prePopup()
			dialog = UpdatesConfirmDialog(gui.mainFrame, on_accept, on_cancel, version=version, title=title, message=message)
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			dialog.Show()
			window.bring_wx_to_top(dialog)
			gui.mainFrame.postPopup()
		queueHandler.queueFunction(queueHandler.eventQueue, h)

class Updates:
	def __init__(self, url):
		self._request_data = None
		self._url = url
		self._thread = None

	def _get_request_data(self, pickle):
		if not self._request_data:
			self._request_data = version.composed_version()
			self._request_data["addon"]["update_version"] = 1
			if pickle:
				self._request_data["addon"]["since"] = pickle.cdata["updates"]["since"]
		return self._request_data

	def check(self, cb, pickle=None):
		def _check_proc():
			cb_data = self._get_request_data(pickle)
			response = json_post(self._url, cb_data)
			status = "fail"
			if response:
				try:
					response = json.load(response)
					if response and "status" in response:
						status = response["status"]
						cb_data["update"] = response
						del cb_data["update"]["status"]
				except:
					del cb_data["update"]
					status = "fail"
			if pickle:
				data = pickle.start_write()
				data["updates"]["last_check"] = time.time()
				data["updates"]["last_status"] = status
				pickle.commit_write()
			self._thread = None
			if cb:
				cb(self, status, cb_data)

		if not self._thread:
			self._thread = threading.Thread(target = _check_proc)
			self._thread.setDaemon(True)
			self._thread.start()
			return True
		return False

	def download(self, cb, data, pickle=None):
		url = None
		if data:
			if "update" in data:
				update = data["update"]
				if "url" in update:
					url = update["url"]
				elif "direct_url" in update:
					url = update["direct_url"]
			if not url and "url" in data:
				url = data["url"]
		if url:
			def _download_proc():
				response = json_post(url, data)
				self._thread = None
				if cb:
					cb(self, response)
			
			if not self._thread:
				self._thread = threading.Thread(target = _download_proc)
				self._thread.setDaemon(True)
				self._thread.start()
				return True
		return False

	def install(self, addonPath, cb=None):
		def h():
			ret = addonGui.installAddon(gui.mainFrame, addonPath)
			if cb: cb(ret)
			if ret:
				addonGui.promptUserForRestart()
		wx.CallAfter(h)

class AutoUpdates:
	def __init__(self, url, pickle):
		self._updates = Updates(url)
		self._pickle = pickle
		self._timer = None

	def stop(self):
		if self._timer and self._timer.IsRunning():
			self._timer.Stop()
		self._timer = None

	def start(self):
		if not self._timer:
			self._timer = wx.PyTimer(self.check)
			wx.CallAfter(self._timer.Start, 5000, True)

	def check(self):
		if globalVars.appArgs.secure:
			wx.CallAfter(self._timer.Start, 5000, True)
		else:
			data = self._pickle.cdata["updates"]
			secsSinceLast = max(time.time() - data["last_check"], 0)
			if data["last_status"] == "ok" or data["last_status"] == "upgrade":
				secsTillNext = CHECK_INTERVAL - int(min(secsSinceLast, CHECK_INTERVAL))
			else:
				secsTillNext = CHECK_INTERVAL_FAIL - int(min(secsSinceLast, CHECK_INTERVAL_FAIL))
			if secsTillNext < 10:
				secsTillNext = 10
			self._timer = wx.PyTimer(self._updates_proc)
			wx.CallAfter(self._timer.Start, secsTillNext * 1000, True)

	def _updates_proc(self):
		def _end_proc(restart=True):
			if self._timer:
				self._timer = None
				if restart:
					self.start()
		
		if self._timer:
			def check_cb(updates, status, data):
				if status == "upgrade":
					last_version = None
					if data and "update" in data and "last_version" in data["update"] and data["update"]["last_version"]:
						last_version = data["update"]["last_version"]
					
					def do_update():
						if data and "addon" in data and "name" in data["addon"] and data["addon"]["name"]:
							tmp_file = data["addon"]["name"]
						else:
							tmp_file = addonHandler.getCodeAddon().manifest["summary"]
						if last_version:
							tmp_file = tmp_file + "-" + last_version
						else:
							tmp_file = tmp_file + "-update"
						tmp_file = os.path.join(tempfile.gettempdir(), tmp_file + ".nvda-addon")
						
						def remove_file():
							if os.path.isfile(tmp_file):
								try:
									os.chmod(tmp_file, stat.S_IWRITE)
									os.remove(tmp_file)
								except:
									pass
						
						def download_cb(updates, response):
							def install_cb(installed):
								remove_file()
								_end_proc(restart=not installed)
							
							if response and response.status == 200:
								try:
									package = response.read()
								except:
									package = None
								if package:
									try:
										f = open(tmp_file, 'wb')
										f.write(package)
										f.close()
										self._updates.install(tmp_file, install_cb)
										return
									except:
										remove_file()
							_end_proc()
						
						remove_file()
						if not self._updates.download(download_cb, data, self._pickle):
							_end_proc()
					
					UpdatesConfirmDialog.Ask(do_update, _end_proc, version=last_version)
				else:
					_end_proc()
			
			self._updates.check(check_cb, self._pickle)