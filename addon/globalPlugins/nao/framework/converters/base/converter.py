#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-21
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import threading
import subprocess
import time

class Converter:
	def __init__(self, temp_sub_path, clear_on_destruct=True):
		self._instance_id = str(round(time.time() * 1000))
		self._clear_on_destruct = clear_on_destruct

		self._addon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
		self._temp_path = os.path.join(self._addon_path, temp_sub_path)
		
		self._source_file = None
		self._on_finish = None
		self._on_progress = None
		self._progress_timeout = 1

	def __del__(self):
		if self._clear_on_destruct:
			self.clear()

	@property
	def instance_id(self):
		return self._instance_id

	@property
	def source_file(self):
		return self._source_file

	@property
	def temp_path(self):
		return self._temp_path

	@property
	def count(self):
		return False

	@property
	def results(self):
		ret = []
		if os.path.isdir(self._temp_path):
			for f in os.listdir(self._temp_path):
				fc = os.path.join(self._temp_path, f)
				if os.path.isfile(fc) and f.startswith(self._instance_id):
					ret.append(fc)
		return ret

	def clear(self):
		if os.path.isdir(self._temp_path):
			for f in self.results:
				try:
					os.remove(f)
				except:
					pass
			try:
				os.rmdir(self._temp_path)
			except:
				pass

	def clear_all(self):
		if os.path.isdir(self._temp_path):
			for f in os.listdir(self._temp_path):
				try:
					os.remove(os.path.join(self._temp_path, f))
				except:
					pass
			try:
				os.rmdir(self._temp_path)
			except:
				pass

	def abort(self):
		self._thread = None

	def _convert(self, source_file, type, on_finish=None, on_progress=None, progress_timeout=1):
		self._source_file = source_file
		self._type = type
		self._on_finish = on_finish
		self._on_progress = on_progress
		self._progress_timeout = progress_timeout
		self._thread = threading.Thread(target = self._thread)
		self._thread.setDaemon(True)
		self._thread.start()

	def _thread(self):
		self.clear()
		if not os.path.isdir(self._temp_path):
			os.mkdir(self._temp_path)
		
		if self._on_progress:
			self._on_progress(self, 0, self.count)
		
		# The next two lines are to prevent the cmd from being displayed.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		
		p = subprocess.Popen(self._command(self._type), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=si)
		while self._thread:
			try:
				p.wait(timeout=self._progress_timeout)
				break
			except subprocess.TimeoutExpired:
				if self._thread and self._on_progress:
					self._on_progress(self, len(self.results), self.count)
		
		if self._thread:
			if self._on_progress:
				self._on_progress(self, len(self.results), self.count)
			if self._on_finish:
				self._on_finish(success=(p.returncode == 0), converter=self)
		else:
			p.kill()
		
		self._type = None
		self._on_finish = None
		self._on_progress = None
		if not self._thread:
			self.clear()
		else:
			self._thread = None