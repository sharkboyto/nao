#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-14
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import threading

class AsyncResult:
	def __init__(self):
		self._terminate_event = threading.Event()
		self._terminated_event = threading.Event()
		self._value = None

	def terminate(self):
		self._terminate_event.set()

	def wait(self, timeout=None):
		return self._terminated_event.wait(timeout=timeout)

	@property
	def Value(self):
		return self._value

class AsyncWait:
	def __init__(self, async_result):
		self.async_result = async_result

	def must_terminate(self, timeout=0):
		return self.async_result._terminate_event.wait(timeout=timeout)

	def terminated(self, value):
		self.async_result._value = value
		self.async_result._terminated_event.set()

class Thread(threading.Thread):
	def __init__(self):
		self._result = AsyncResult()
		def h():
			self.proc(AsyncWait(self._result))
			self._result._terminated_event.set()
		super(Thread, self).__init__(target=h)
		self.setDaemon(True)

	@property
	def AsyncResult(self):
		return self._result

	def proc(self, wait):
		pass

	def terminate(self):
		self._result.terminate()

	def wait(self, timeout=None):
		return self._result.wait(timeout=timeout)