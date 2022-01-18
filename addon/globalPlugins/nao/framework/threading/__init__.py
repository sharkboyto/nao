#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-18
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
	StatusStarting = 'starting'
	StatusRunning = 'running'
	StatusFinished = 'finished'
	StatusCancelled = 'cancelled'
	StatusException = 'exception'

	def __init__(self):
		self._terminate_event = ProgramTerminateEvent()
		self._terminated_event = threading.Event()
		self._status = AsyncResult.StatusIdle
		self._value = None
		self._exception = None
		self._lock = threading.RLock()

	def terminate(self):
		self._lock.acquire()
		self._status = AsyncResult.StatusCancelled
		self._lock.release()
		self._terminate_event.set()

	def wait(self, timeout=None):
		return self._terminated_event.wait(timeout=timeout)

	@property
	def Status(self):
		self._lock.acquire()
		ret = self._status
		self._lock.release()
		return ret

	@property
	def Value(self):
		self._lock.acquire()
		ret = self._value
		self._lock.release()
		return ret

	@property
	def Exception(self):
		self._lock.acquire()
		ret = self._exception
		self._lock.release()
		return ret

class AsyncWait:
	def __init__(self, async_result):
		self._result = async_result

	def must_terminate(self, timeout=0):
		return self._result._terminate_event.wait(timeout=timeout)

	def set_value(self, value):
		self._result._lock.acquire()
		self._result._value = value
		self._result._lock.release()

	def set_value_dict(self, value, class_name='Value'):
		if value is not None:
			from collections import namedtuple
			self.set_value(namedtuple(class_name, value)(**value))
		else:
			self.set_value(None)

class Thread(threading.Thread):
	def __init__(self, target=None, on_finish=None, name=None):
		self._result = AsyncResult()
		wait = AsyncWait(self._result)
		def h():
			self._result._lock.acquire()
			self._result._status = AsyncResult.StatusRunning
			self._result._lock.release()
			try:
				if target:
					target(wait=wait)
				else:
					self.thread_proc(wait=wait)
			except Exception as e:
				self._result._lock.acquire()
				self._result._exception = e
				self._result._status = AsyncResult.StatusException
				self._result._lock.release()
				raise
			finally:
				self._result._lock.acquire()
				if self._result._status == AsyncResult.StatusRunning:
					if self._result._terminate_event.is_set():
						self._result._status = AsyncResult.StatusCancelled
					else:
						self._result._status = AsyncResult.StatusFinished
				self._result._lock.release()
				if on_finish: on_finish(result=self._result)
				self._result._terminated_event.set()
		super(Thread, self).__init__(target=h, name=name)
		self.setDaemon(True)

	@property
	def Status(self):
		return self._result.Status

	def thread_proc(self, wait):
		pass

	def start(self):
		self._result._lock.acquire()
		if self._result._status == AsyncResult.StatusIdle: self._result._status = AsyncResult.StatusStarting
		self._result._lock.release()
		try:
			super(Thread, self).start()
		except Exception as e:
			self._result._lock.acquire()
			self._result._exception = e
			self._result._status = AsyncResult.StatusException
			self._result._lock.release()
			self._result._terminated_event.set()
			raise
		return self._result

	def terminate(self):
		self._result.terminate()

	def wait(self, timeout=None):
		return self._result.wait(timeout=timeout)