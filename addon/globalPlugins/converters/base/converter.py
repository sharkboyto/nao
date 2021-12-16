#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-16
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


	def _convert(self, source_file, type, on_finish=None):
		self._source_file = source_file
		self._type = type
		self._on_finish = on_finish
		self._thread = threading.Thread(target = self._thread)
		self._thread.setDaemon(True)
		self._thread.start()

	def _thread(self):
		self.clear()
		if not os.path.isdir(self._temp_path):
			os.mkdir(self._temp_path)
		
		# The next two lines are to prevent the cmd from being displayed.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		
		p = subprocess.Popen(self._command(self._type), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
		stdout, stderr = p.communicate()
		
		if self._on_finish:
			self._on_finish(success=(p.returncode == 0), converter=self)
			self._on_finish = None
		
		self._type = None