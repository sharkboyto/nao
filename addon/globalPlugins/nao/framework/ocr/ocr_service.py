#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import weakref
import winVersion
import threading
import winGDI
import wx
from contentRecog import uwpOcr, recogUi

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
		self._queue_push = threading.Event()
		self._pixels = None
		self._pixels_size = [0, 0]
		self._fake_recog = FakeRecog()

	def push_bitmap(self, bitmap, on_recognize_result):
		if bitmap and on_recognize_result:
			width, height = bitmap.Size.Get()
			self._queue_lock.acquire()
			self._queue.append([bitmap, None, width, height, on_recognize_result])
			self._queue_push.set()
			self._thread_start()
			self._queue_lock.release()

	def push_pixels(self, pixels, width, height, on_recognize_result):
		if pixels and on_recognize_result:
			self._queue_lock.acquire()
			self._queue.append([None, pixels, width, height, on_recognize_result])
			self._queue_push.set()
			self._thread_start()
			self._queue_lock.release()

	def _thread_start(self):
		if not self._thread:
			self._thread = threading.Thread(target = self._threadproc)
			self._thread.setDaemon(True)
			self._thread.start()

	def _recognize(self, bmp, pixels, width, height, on_recognize_result):
		if not pixels and bmp:
			if not self._pixels or self._pixels_size[0] != width or self._pixels_size[1] != height:
				try:
					self._pixels = (winGDI.RGBQUAD*width*height)()
					self._pixels_size = [width, height]
				except MemoryError as e:
					on_recognize_result(e)
					self._pixels = None
			if self._pixels:
				bmp.CopyToBuffer(self._pixels, format=wx.BitmapBufferFormat_ARGB32)
				pixels = self._pixels
		if pixels:
			recognizer = uwpOcr.UwpOcr()
			try:
				imgInfo = recogUi.RecogImageInfo.createFromRecognizer(0, 0, width, height, recognizer)
			except ValueError as e:
				on_recognize_result(e)
				return
			event = threading.Event()
			def h(result):
				on_recognize_result(result)
				event.set()
			try:
				recognizer.recognize(pixels, imgInfo, h)
				event.wait()
			except Exception as e:
				on_recognize_result(e)

	def _threadproc(self):
		must_exit = False
		self._queue_lock.acquire()
		while not must_exit:
			while not recogUi._activeRecog and len(self._queue) > 0:
				recogUi._activeRecog = self._fake_recog
				bmp, pixels, width, height, on_recognize_result = self._queue.pop(0)
				self._queue_lock.release()
				if (bmp or pixels) and on_recognize_result:
					self._recognize(bmp, pixels, width, height, on_recognize_result)
				self._queue_lock.acquire()
				recogUi._activeRecog = None
				try:
					self._fake_recog._lock.release()
				except RuntimeError:
					pass
				if self._fake_recog._cancelled:
					break
			self._queue_push.clear()
			self._queue_lock.release()
			self._queue_push.wait(timeout=5)
			self._queue_lock.acquire()
			self._fake_recog._lock.acquire(blocking=False)
			self._fake_recog._cancelled = False
			must_exit = len(self._queue) == 0
		self._thread = None
		self._pixels = None
		self._queue_lock.release()