#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-29
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import weakref
import threading
import os
import globalVars
import pickle
import copy
from .. collections import dictionaries

class Pickle:
	_instances = {}
	_instances_lock = threading.Lock()

	def __new__(cls, name):
		ret = None
		cls._instances_lock.acquire()
		if name in cls._instances:
			ret =  cls._instances[name]()
		cls._instances_lock.release()
		if ret is None:
			ret = super(Pickle, cls).__new__(cls)
		return ret

	def __init__(self, name):
		Pickle._instances_lock.acquire()
		if name not in Pickle._instances or Pickle._instances[name]() is None:
			Pickle._instances[name] = weakref.ref(self)
			self._name = name
			self._lock = threading.Lock()
			self._data = None
			self._pickle_file_name = None
		Pickle._instances_lock.release()

	@property
	def pickle_file_name(self):
		if not self._pickle_file_name:
			self._pickle_file_name = os.path.join(globalVars.appArgs.configPath, self._name + ".pickle")
		return self._pickle_file_name

	@property
	def pickle_file_exists(self):
		return os.path.isfile(self.pickle_file_name)

	@property
	def default_data(self):
		return {}

	@property
	def cdata(self):
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
			os.remove(self.pickle_file_name)
		except:
			pass
		self._data = None
		self._lock.release()

	def _load(self):
		try:
			with open(self.pickle_file_name, "rb") as f:
				self._data = pickle.load(f)
				self._data = dictionaries.merge(self.default_data, self._data)
		except:
			self._data = self.default_data

	def _save(self):
		if self._data:
			try:
				with open(self.pickle_file_name, "wb") as f:
					pickle.dump(self._data, f, protocol=0)
				return True
			except:
				pass
		return False