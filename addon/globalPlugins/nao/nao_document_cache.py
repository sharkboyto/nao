#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-27
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

from .framework.storage.file_cache import FileCache

class NaoDocumentCache:
	class Cache(FileCache): pass

	PURGE_INTERVAL = 4*86400 # 4 day

	def __new__(cls):
		import globalVars
		import os
		return NaoDocumentCache.Cache(os.path.join(globalVars.appArgs.configPath, "nao-document-cache"), max_size=256*1024*1024, max_age=180*86400, max_count=100000)

	def clear():
		def _end_proc(result):
			import time
			from .nao_pickle import NaoPickle
			pickle = NaoPickle()
			pickle.start_write()["cache"]["documents"]["last_purge"] = time.time()
			pickle.commit_write()
		cache = NaoDocumentCache()
		if cache: cache.clear(on_finish=_end_proc)

	def schedule_purge():
		import wx
		import time
		from .nao_pickle import NaoPickle
		
		class Scheduler:
			def __init__(self):
				from .framework.threading import ProgramTerminateHandler
				self._timer = wx.PyTimer(self._check_remaining_time)
				wx.CallAfter(self._timer.Start, 60000, True)
				self._terminate_handler = ProgramTerminateHandler(self.terminate)

			def __del__(self):
				self.terminate()

			def terminate(self):
				if self._terminate_handler:
					self._terminate_handler.unregister()
					self._terminate_handler = None
				if self._timer and self._timer.IsRunning():
					self._timer.Stop()
				self._timer = None

			def _check_remaining_time(self):
				pickle = NaoPickle()
				last_purge = pickle.cdata["cache"]["documents"]["last_purge"]
				if last_purge > 0:
					secsSinceLast = max(time.time() - last_purge, 0)
					secsTillNext = NaoDocumentCache.PURGE_INTERVAL - int(min(secsSinceLast, NaoDocumentCache.PURGE_INTERVAL))
					if secsTillNext < 5:
						secsTillNext = 5
						self._timer = wx.PyTimer(self._purge_proc)
					else:
						self._timer = wx.PyTimer(self._check_remaining_time)
				else:
					pickle.start_write()["cache"]["documents"]["last_purge"] = time.time()
					pickle.commit_write()
					secsTillNext = 60
					self._timer = wx.PyTimer(self._check_remaining_time)
				wx.CallAfter(self._timer.Start, secsTillNext * 1000, True)

			def _purge_proc(self):
				def _end_proc(result):
					self._timer = wx.PyTimer(self._check_remaining_time)
					wx.CallAfter(self._timer.Start, 60000, True)
				pickle = NaoPickle()
				pickle.start_write()["cache"]["documents"]["last_purge"] = time.time()
				pickle.commit_write()
				cache = NaoDocumentCache()
				if cache:
					cache.purge(on_finish=_end_proc)
				else:
					_end_proc(None)
		
		return Scheduler()