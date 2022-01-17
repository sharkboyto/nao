#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import weakref
import winVersion
import threading
import winGDI
import wx
from contentRecog import uwpOcr, recogUi
from .. threading import Thread, ProgramTerminateEvent
from .. import language

language.initTranslation()

class FakeRecog:
	def __init__(self):
		self._lock = threading.Lock()
		self._lock.acquire()
		self._cancelled = False

	def cancel(self):
		self._cancelled = True
		self._lock.acquire()

class OCRService:
	def is_uwp_ocr_available():
		return winVersion.isUwpOcrAvailable()

	def uwp_ocr_config_language():
		return uwpOcr.getConfigLanguage()

	class QueueItem:
		def __init__(self, bitmap=None, pixels=None, width=None, height=None, language=None, on_recognize_result=None):
			if not language: language = OCRService.uwp_ocr_config_language()
			if bitmap and (width is None or height is None): width, height = bitmap.Size.Get()
			self.bitmap = bitmap
			self.pixels = pixels
			self.width = width
			self.height = height
			self.language = language
			self.on_recognize_result = on_recognize_result

	@classmethod
	def _instance(cls):
		return None

	def __new__(cls, *args, **kwargs):
		instance = OCRService._instance()
		if instance is None:
			return super(OCRService, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(self):
		if OCRService._instance() is not None: return
		OCRService._instance = weakref.ref(self)
		self._thread = None
		self._queue = []
		self._queue_lock = threading.Lock()
		self._queue_push = ProgramTerminateEvent()
		self._pixels = None
		self._pixels_size = [0, 0]
		self._fake_recog = FakeRecog()

	def push_bitmap(self, bitmap, on_recognize_result, language=None):
		if bitmap and on_recognize_result:
			self._push(OCRService.QueueItem(bitmap=bitmap, language=language, on_recognize_result=on_recognize_result))
		elif on_recognize_result:
			on_recognize_result(ValueError("Invalid bitmap"))

	def push_pixels(self, pixels, width, height, on_recognize_result, language=None):
		if pixels and on_recognize_result:
			self._push(OCRService.QueueItem(pixels=pixels, width=width, height=height, language=language, on_recognize_result=on_recognize_result))

	def _thread_start(self):
		if not self._thread:
			self._thread = Thread(target=self._threadproc)
			self._thread.start()

	def _push(self, item):
		if item:
			self._queue_lock.acquire()
			self._queue.append(item)
			self._queue_push.set()
			self._thread_start()
			self._queue_lock.release()

	def _recognize(self, item):
		if not item.pixels and item.bitmap:
			if not self._pixels or self._pixels_size[0] != item.width or self._pixels_size[1] != item.height:
				try:
					self._pixels = (winGDI.RGBQUAD*item.width*item.height)()
					self._pixels_size = [item.width, item.height]
				except MemoryError as e:
					item.on_recognize_result(e)
					self._pixels = None
			if self._pixels:
				item.bitmap.CopyToBuffer(self._pixels, format=wx.BitmapBufferFormat_ARGB32)
				item.pixels = self._pixels
		if item.pixels:
			recognizer = uwpOcr.UwpOcr(language=item.language)
			try:
				imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, item.width, item.height, recognizer)
			except ValueError as e:
				item.on_recognize_result(e)
				return
			event = ProgramTerminateEvent()
			def h(result):
				if not isinstance(result, Exception):
					from collections import namedtuple
					result = {
						'data': result,
						'language': item.language,
						'width': item.width,
						'height': item.height
					}
					result = namedtuple('OCRServiceResult', result)(**result)
				item.on_recognize_result(result)
				event.set()
			try:
				recognizer.recognize(item.pixels, imgInfo, h)
				event.wait()
			except Exception as e:
				item.on_recognize_result(e)

	def _threadproc(self, wait):
		self._queue_lock.acquire()
		while not wait.must_terminate() and len(self._queue) > 0:
			while not wait.must_terminate() and len(self._queue) > 0 and not recogUi._activeRecog:
				recogUi._activeRecog = self._fake_recog
				item = self._queue.pop(0)
				self._queue_lock.release()
				if (item.bitmap or item.pixels) and item.on_recognize_result:
					self._recognize(item)
				self._queue_lock.acquire()
				recogUi._activeRecog = None
				try:
					self._fake_recog._lock.release()
				except RuntimeError:
					pass
				if self._fake_recog._cancelled:
					break
			self._queue_push.clear()
			if not wait.must_terminate():
				self._queue_lock.release()
				self._queue_push.wait(timeout=5)
				self._queue_lock.acquire()
			self._fake_recog._lock.acquire(blocking=False)
			self._fake_recog._cancelled = False
		self._thread = None
		self._pixels = None
		self._queue_lock.release()