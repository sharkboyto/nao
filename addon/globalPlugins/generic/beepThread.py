#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-11-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import threading
import tones
import time

class BeepThread:
	def __init__(self):
		self._thread = None

	def start(self):
		if not self._thread:
			self._thread = threading.Thread(target = self._threadproc)
			self._thread.setDaemon(True)
			self._thread.start()

	def stop(self):
		self._thread = None

	def _threadproc(self):
		while self._thread:
			tones.beep(440, 40)
			time.sleep(1)
