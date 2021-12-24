#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-24
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import json
import threading
import time
import os
import pickle

from . import version
from .http import json_post

CHECK_INTERVAL = 86400 # 1 day

class Updates:
	def __init__(self, url):
		self._request_data = None
		self._url = url
		self._thread = None

	def _get_request_data(self):
		if not self._request_data:
			self._request_data = version.composed_version()
			self._request_data["addon"]["update_version"] = 0
		return self._request_data

	def check(self, cb):
		def _check_proc():
			url = None
			response = json_post(self._url, self._get_request_data())
			if response:
				try:
					response = json.load(response)
					url = response.url
				except:
					pass
			self._thread = None
			if cb:
				cb(self, url)

		if not self._thread:
			self._thread = threading.Thread(target = _check_proc)
			self._thread.setDaemon(True)
			self._thread.start()

	def download(self):
		#TODO
		return False
		
class AutoUpdates:
	def __init__(self, url):
		self._updates = Updates(url)
		self._state = None
		self._stateFileName = os.path.abspath(os.path.join(os.path.dirname(__file__), "updates_state.pickle"))
		self._terminate_event = threading.Event()
		self._done_event = threading.Event()
		self._thread = threading.Thread(target = self._auto_updates_proc)
		self._thread.setDaemon(True)
		self._thread.start()

	def destroy(self):
		self._terminate_event.set()
		self._done_event.set()

	def _save_state(self):
		if self._state:
			try:
				with open(self._stateFileName, "wb") as f:
					pickle.dump(self._state, f, protocol=0)
				return True
			except:
				pass
		return False

	def _load_state(self):
		if not self._state:
			try:
				with open(self._stateFileName, "rb") as f:
					self._state = pickle.load(f)
			except:
				self._state = {
					"lastCheck": 0
				}

	def _auto_updates_proc(self):
		self._load_state()
		while not self._terminate_event.wait(0):
			secsSinceLast = time.time()
			if self._state and "lastCheck" in self._state:
				secsSinceLast = max(secsSinceLast - self._state["lastCheck"], 0)
			secsTillNext = CHECK_INTERVAL - int(min(secsSinceLast, CHECK_INTERVAL))
			if secsTillNext < 10:
				secsTillNext = 10
			if self._terminate_event.wait(secsTillNext):
				break
			def cb(updates, url):
				self._state["lastCheck"] = time.time()
				self._save_state()
				#TODO
				#print(url)
				self._done_event.set()
			self._updates.check(cb)
			self._done_event.wait()
			self._done_event.clear()