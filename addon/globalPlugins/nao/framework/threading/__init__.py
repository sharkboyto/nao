#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-15
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import threading

GLOBAL_HANDLER_PROGRAM_TERMINATE = "program_terminate"

class GlobalHandler():
	_handlers = {}
	_handlers_lock = threading.RLock()

	def __init__(self, name, handler=None):
		import weakref
		self.global_name = name
		self.global_handler = None
		self._self_weak = weakref.ref(self)
		if handler:
			self.register(handler)

	def __del__(self):
		self.unregister()

	def register(self, handler):
		GlobalHandler._handlers_lock.acquire()
		self.global_handler = handler
		if not self.global_name in GlobalHandler._handlers: GlobalHandler._handlers[self.global_name] = set()
		GlobalHandler._handlers[self.global_name].add(self._self_weak)
		GlobalHandler._handlers_lock.release()

	def unregister(self):
		GlobalHandler._handlers_lock.acquire()
		self.global_handler = None
		if self.global_name in GlobalHandler._handlers:
			GlobalHandler._handlers[self.global_name].discard(self._self_weak)
			if len(GlobalHandler._handlers[self.global_name]) == 0: del GlobalHandler._handlers[self.global_name]
		GlobalHandler._handlers_lock.release()

	def call_handler(self):
		if self.global_handler: self.global_handler()

	def call(name, remove_handlers=False):
		if name:
			GlobalHandler._handlers_lock.acquire()
			if name in GlobalHandler._handlers:
				handlers = GlobalHandler._handlers[name].copy()
				if remove_handlers:
					GlobalHandler._handlers[name].clear()
					del GlobalHandler._handlers[name]
			else:
				handlers = None
			GlobalHandler._handlers_lock.release()
			if handlers:
				for h in handlers:
					h = h()
					if h: h.call_handler()

class GlobalEvent(threading.Event):
	def __init__(self, name):
		super(GlobalEvent, self).__init__()
		self.global_handler = GlobalHandler(name, handler=self.set)

	def set(self):
		self.global_handler.unregister()
		super(GlobalEvent, self).set()

	def clear(self):
		self.global_handler.register(self.set)
		super(GlobalEvent, self).clear()

def ProgramTerminateHandler(handler):
	return GlobalHandler(GLOBAL_HANDLER_PROGRAM_TERMINATE, handler=handler)

def ProgramTerminateEvent():
	return GlobalEvent(GLOBAL_HANDLER_PROGRAM_TERMINATE)

def ProgramTerminate():
	GlobalHandler.call(GLOBAL_HANDLER_PROGRAM_TERMINATE, True)

class AsyncResult:
	StatusIdle = 'idle'
	StatusRunning = 'running'
	StatusFinished = 'finished'
	StatusCancelled = 'cancelled'
	StatusException = 'exception'

	def __init__(self):
		self._terminate_event = ProgramTerminateEvent()
		self._terminated_event = threading.Event()
		self._value = None
		self._status = AsyncResult.StatusIdle
		self._exception = None

	def terminate(self):
		self._terminate_event.set()

	def wait(self, timeout=None):
		return self._terminated_event.wait(timeout=timeout)

	@property
	def Value(self):
		return self._value

	@property
	def Status(self):
		return self._status

	@property
	def Exception(self):
		return self._exception

class AsyncWait:
	def __init__(self, async_result):
		self.async_result = async_result

	def must_terminate(self, timeout=0):
		return self.async_result._terminate_event.wait(timeout=timeout)

	def set_value(self, value):
		self.async_result._value = value

	def set_status(self, status):
		self.async_result._status = status

	def set_exception(self, exception):
		self.async_result._exception = exception

	def terminated(self):
		self.async_result._terminated_event.set()

class Thread(threading.Thread):
	def __init__(self, target=None, on_finish=None):
		self._result = AsyncResult()
		def h():
			wait = AsyncWait(self._result)
			try:
				if target:
					target(wait=wait)
				else:
					self.thread_proc(wait=wait)
			except:
				raise
			finally:
				wait.terminated()
				if on_finish: on_finish(result=self._result)
		super(Thread, self).__init__(target=h)
		self.setDaemon(True)

	@property
	def AsyncResult(self):
		return self._result

	def thread_proc(self, wait):
		pass

	def terminate(self):
		self._result.terminate()

	def wait(self, timeout=None):
		return self._result.wait(timeout=timeout)