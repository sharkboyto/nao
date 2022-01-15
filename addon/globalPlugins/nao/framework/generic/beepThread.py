#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-15
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import tones
from .. threading import Thread

class BeepThread:
	def __init__(self):
		self._thread = None

	def __del__(self):
		self.stop()

	def start(self):
		if not self._thread:
			def h(wait):
				while not wait.must_terminate(timeout=1):
					tones.beep(440, 40)
			self._thread = Thread(target=h)
			self._thread.start()

	def stop(self):
		if self._thread:
			self._thread.terminate()
			self._thread = None