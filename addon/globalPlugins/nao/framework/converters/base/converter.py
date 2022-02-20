#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-25
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os

class Converter:
	def __init__(self, temp_sub_path):
		import time
		self._instance_id = str(round(time.time() * 1000))
		self._addon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
		self._tmp_directory = None
		self._temp_sub_path = temp_sub_path
		self._temp_path = os.path.join(self._addon_path, self._temp_sub_path)
		self._source_file = None
		self._on_finish = None
		self._on_progress = None
		self._progress_timeout = 1
		self._thread = None

	def __del__(self):
		self.clear()

	@property
	def instance_id(self):
		return self._instance_id

	@property
	def version(self):
		return None

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
		if self._tmp_directory:
			self._tmp_directory = None
		elif os.path.isdir(self._temp_path):
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
		if self._thread:
			self._thread.terminate()
			self._thread = None

	def _convert(self, source_file, file_type, on_finish=None, on_progress=None, progress_timeout=1):
		from ... threading import Thread
		self._failed = False
		self._aborted = False
		self._source_file = source_file
		self._type = file_type
		self._on_finish = on_finish
		self._on_progress = on_progress
		self._progress_timeout = progress_timeout
		self._thread = Thread(target=self._thread_proc, name=type(self).__name__)
		self._thread.start()

	def _thread_proc(self, wait):
		self.clear()
		process = None
		if not self._failed and not self._aborted:
			if not self._tmp_directory:
				try:
					from tempfile import TemporaryDirectory
					self._tmp_directory = TemporaryDirectory()
					self._temp_path = self._tmp_directory.name
				except:
					self._tmp_directory = None
					self._temp_path = os.path.join(self._addon_path, self._temp_sub_path)
				
				if not self._tmp_directory:
					if not os.path.isdir(self._temp_path):
						os.mkdir(self._temp_path)
			
			if self._on_progress:
				self._on_progress(self, 0, self.count)
			
			if wait.must_terminate():
				self._aborted = True
			else:
				import subprocess
				# The next two lines are to prevent the cmd from being displayed.
				si = subprocess.STARTUPINFO()
				si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				
				try:
					process = subprocess.Popen(self._command(self._type), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=si)
				except:
					process = None
					self._failed = True
				
				if process:
					while not wait.must_terminate():
						try:
							process.wait(timeout=self._progress_timeout)
							break
						except subprocess.TimeoutExpired:
							if not wait.must_terminate() and self._on_progress:
								self._on_progress(self, len(self.results), self.count)
					
					if not wait.must_terminate():
						if self._on_progress:
							self._on_progress(self, len(self.results), self.count)
						if self._on_finish:
							self._on_finish(success=(process.returncode == 0), aborted=False, converter=self)
					else:
						self._aborted = True
						process.kill()
						process.wait(timeout=5)
						#def h():
						#	process.wait(timeout=5)
						#	self.clear()
						#from ... threading import AsyncCall
						#AsyncCall(h)
		
		if (self._failed or self._aborted) and self._on_finish:
			self._on_finish(success=False, aborted=self._aborted, converter=self)
		self._type = None
		self._on_finish = None
		self._on_progress = None
		if self._failed or self._aborted or wait.must_terminate():
			self.clear()
		self._thread = None