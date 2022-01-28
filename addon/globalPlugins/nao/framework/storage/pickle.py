#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-28
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import pickle
from .. generic.singleton_class import SingletonClass

class Pickle(SingletonClass):
	def __singleton_init__(self, path, name):
		from threading import Lock
		self._path = path
		self._file_name = os.path.join(path, name)
		self._data = None
		self._lock = Lock()
		super(Pickle, self).__singleton_init__(path, name)

	def __new__(cls, path, name):
		if path and name:
			return super(Pickle, cls).__new__(cls)
		return None

	@property
	def path(self):
		return self._path

	@property
	def file_name(self):
		return self._file_name

	@property
	def file_exists(self):
		try:
			return os.path.isfile(self.file_name)
		except:
			return None

	@property
	def default_data(self):
		return {}

	@property
	def cdata(self):
		import copy
		self._lock.acquire()
		if not self._data:
			self._load()
		ret = copy.deepcopy(self._data)
		self._lock.release()
		return ret

	def start_write(self):
		self._lock.acquire()
		if not self._data:
			self._load()
		return self._data

	def commit_write(self):
		if self._lock.locked():
			self._save()
			self._lock.release()

	def cancel_write(self):
		if self._lock.locked():
			self._data = None
			self._lock.release()

	def remove(self):
		self._lock.acquire()
		try:
			os.remove(self.file_name)
		except:
			pass
		self._data = None
		self._lock.release()

	def _load(self):
		from .. collections import dictionaries
		try:
			with open(self.file_name, "rb") as f:
				self._data = pickle.load(f)
				self._data = dictionaries.merge(self.default_data, self._data)
		except:
			self._data = self.default_data

	def _save(self):
		if self._data:
			try:
				self._makedirs()
				with open(self.file_name, "wb") as f:
					pickle.dump(self._data, f, protocol=0)
				return True
			except:
				pass
		return False

	def _makedirs(self):
		try:
			os.makedirs(self.path, exist_ok=True)
			return True
		except:
			return False