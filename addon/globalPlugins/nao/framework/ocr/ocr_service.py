#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-04-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import winGDI
import wx
from contentRecog import recogUi
from threading import Lock
from .. import language
from .. generic.singleton_class import SingletonClass

language.initTranslation()

class FakeRecog:
	def __init__(self):
		self._lock = Lock()
		self._lock.acquire()
		self._cancelled = False

	def cancel(self):
		self._cancelled = True
		self._lock.acquire()

class OCRService(SingletonClass):
	def uwp_ocr_config_language():
		from contentRecog import uwpOcr
		return uwpOcr.getConfigLanguage()

	class QueueItem:
		def __init__(self, bitmap=None, pixels=None, x=0, y=0, width=None, height=None, language=None, on_recognize_result=None):
			if not language: language = OCRService.uwp_ocr_config_language()
			if bitmap and (width is None or height is None): width, height = bitmap.Size.Get()
			self.bitmap = bitmap
			self.pixels = pixels
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.language = language
			self.on_recognize_result = on_recognize_result

	class Queue:
		def __init__(self):
			from .. threading import ProgramTerminateEvent
			self.items = []
			self.items_push_event = ProgramTerminateEvent()

		def push(self, item):
			if item:
				self.items.append(item)
				self.items_push_event.set()
				return True
			return False

		@property
		def len(self):
			return len(self.items)

		def pop(self):
			return self.items.pop(0)

		@property
		def push_event(self):
			return self.items_push_event

	class PixelsBuffer:
		def __init__(self):
			self.clear()

		def clear(self):
			self.buffer = None
			self.size = [0, 0]

		def resize(self, item):
			if not self.buffer or self.size[0] != item.width or self.size[1] != item.height:
				try:
					self.buffer = (winGDI.RGBQUAD*item.width*item.height)()
					self.size = [item.width, item.height]
				except MemoryError as e:
					item.on_recognize_result(e)
					self.buffer = None
			return self.buffer is not None

		def copy_from_bitmap(self, item):
			if item.bitmap and self.resize(item):
				item.bitmap.CopyToBuffer(self.buffer, format=wx.BitmapBufferFormat_ARGB32)
				return True
			return False

	def __singleton_init__(self, *args, **kwargs):
		self._ocr_thread = None
		self._queue = OCRService.Queue()
		self._pixels_buffer = OCRService.PixelsBuffer()
		if self.is_uwp(): self._fake_recog = FakeRecog()
		super(OCRService, self).__singleton_init__(*args, **kwargs)

	def is_uwp(self):
		return False

	def needs_pixels(self):
		return False

	def recognize(self, item):
		raise NotImplementedError()

	def push_bitmap(self, bitmap, on_recognize_result, x=0, y=0, language=None):
		if bitmap and on_recognize_result:
			self.push_item(OCRService.QueueItem(bitmap=bitmap, x=x, y=y, language=language, on_recognize_result=on_recognize_result))
		elif on_recognize_result:
			on_recognize_result(ValueError("Invalid bitmap"))

	def push_pixels(self, pixels, width, height, on_recognize_result, x=0, y=0, language=None):
		if pixels and on_recognize_result:
			self.push_item(OCRService.QueueItem(pixels=pixels, x=x, y=y, width=width, height=height, language=language, on_recognize_result=on_recognize_result))

	def push_item(self, item):
		if item:
			self.Lock.acquire()
			if self._queue.push(item):
				self._ocr_thread_start()
			self.Lock.release()

	def _ocr_thread_start(self):
		from .. threading import Thread
		if not self._ocr_thread:
			self._ocr_thread = Thread(target=self._ocr_thread_proc)
			self._ocr_thread.start()

	def _ocr_thread_proc(self, wait):
		self.Lock.acquire()
		while not wait.must_terminate() and self._queue.len > 0:
			while not wait.must_terminate() and self._queue.len > 0:
				if self.is_uwp():
					if recogUi._activeRecog: break
					recogUi._activeRecog = self._fake_recog
				item = self._queue.pop()
				self.Lock.release()
				if (item.bitmap or item.pixels) and item.on_recognize_result:
					if self.needs_pixels() and not item.pixels and self._pixels_buffer.copy_from_bitmap(item): item.pixels = self._pixels_buffer.buffer
					self.recognize(item)
				self.Lock.acquire()
				if self.is_uwp():
					recogUi._activeRecog = None
					try:
						self._fake_recog._lock.release()
					except RuntimeError:
						pass
					if self._fake_recog._cancelled:
						break
			self._queue.push_event.clear()
			if not wait.must_terminate():
				self.Lock.release()
				self._queue.push_event.wait(timeout=5)
				self.Lock.acquire()
			if self.is_uwp():
				self._fake_recog._lock.acquire(blocking=False)
				self._fake_recog._cancelled = False
		self._ocr_thread = None
		self._pixels_buffer.clear()
		self.Lock.release()