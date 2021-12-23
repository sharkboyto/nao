#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import threading
import tones

class BeepThread:
	def __init__(self):
		self._thread = None
		self._thread_event = threading.Event()

	def start(self):
		if not self._thread:
			self._thread = threading.Thread(target = self._threadproc)
			self._thread.setDaemon(True)
			self._thread.start()

	def stop(self):
		if self._thread:
			self._thread_event.set()

	def _threadproc(self):
		while not self._thread_event.wait(timeout=1):
			tones.beep(440, 40)
		self._thread_event.clear()
		self._thread = None