#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-26
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import time
from threading import RLock
from . import storage_utils
from .. threading import Thread, AsyncCall
from .. generic.singleton_class import SingletonClass

class FileCache(SingletonClass):
	OBJ_EXTENSION = 'obj'
	METADATA_EXTENSION = 'metadata'

	class Source:
		def __init__(self, file, key, metadata=None):
			if not file: raise ValueError('not valid file')
			if not key: raise ValueError('not valid key')
			self.file = file
			self.key = key.lower()
			if metadata:
				if isinstance(metadata, dict):
					self.metadata = metadata
				else:
					raise ValueError('metadata value must be a dictionary')
			else:
				self.metadata = None

		@property
		def exists(self):
			try:
				if self.file:
					return os.path.isfile(self.file)
			except:
				pass
			return False

	class Item:
		def __init__(self, file_cache, key, metadata=None, temp=False):
			self.file_cache = file_cache
			self.key = key.lower()
			self.metadata = metadata
			self.temp = temp
			self.obj_file = os.path.join(self.file_cache.path, self.key + '.' + FileCache.OBJ_EXTENSION) if self.key else None
			self.metadata_file = os.path.join(self.file_cache.path, self.key + '.' + FileCache.METADATA_EXTENSION) if self.key else None
			if self.temp and self.obj_file and self.metadata_file:
				self.file_cache._add_lock.acquire()
				id = str(self.file_cache._add_seq)
				self.file_cache._add_seq += 1
				self.file_cache._add_lock.release()
				self.obj_file += '.' + id + '.add'
				self.metadata_file += '.' + id + '.add'
			self.utime = 0
			self._size = 0

		@property
		def exists(self):
			ret = False
			if self.obj_file:
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					ret = os.path.isfile(self.obj_file)
				except:
					ret = False
				if not self.temp: self.file_cache.Lock.release()
			return ret

		@property
		def mtime(self):
			ret = 0
			if self.obj_file:
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					ret = os.stat(self.obj_file).st_mtime
				except:
					ret = 0
				if not self.temp: self.file_cache.Lock.release()
			return ret

		@property
		def size(self):
			ret = self._size
			if ret == 0 and self.obj_file:
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					ret = os.stat(self.obj_file).st_size
				except:
					ret = 0
				if not self.temp: self.file_cache.Lock.release()
			return ret

		def remove(self):
			if self.obj_file or self.metadata_file:
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					if self.obj_file and os.path.isfile(self.obj_file):
						os.remove(self.obj_file)
				except:
					pass
				try:
					if self.metadata_file and os.path.isfile(self.metadata_file):
						os.remove(self.metadata_file)
				except:
					pass
				if not self.temp: self.file_cache.Lock.release()

		def save_metadata(self, metadata_file=None):
			check_obj_exists = False
			if not metadata_file:
				metadata_file = self.metadata_file
				check_obj_exists = True
			ret = False
			if metadata_file:
				now = time.time()
				metadata = {
					'utime': now
				}
				if self.metadata:
					metadata['metadata'] = self.metadata
				import json
				try:
					metadata = json.dumps(metadata)#, indent=4)
				except:
					metadata = None
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					if os.path.isfile(metadata_file):
						os.remove(metadata_file)
				except:
					pass
				if metadata and (not check_obj_exists or self.exists):
					try:
						with open(metadata_file, "w", encoding="UTF-8") as f:
							f.write(metadata)
						self.utime = now
						ret = True
					except:
						pass
					if not ret:
						try:
							if os.path.isfile(metadata_file):
								os.remove(metadata_file)
						except:
							pass
				if not self.temp: self.file_cache.Lock.release()
			return ret

		def load_metadata(self):
			if self.metadata_file:
				metadata = None
				if not self.temp: self.file_cache.Lock.acquire()
				try:
					if self.exists and os.path.isfile(self.metadata_file):
						with open(self.metadata_file, "r", encoding="UTF-8") as f:
							metadata = f.read()
				except:
					pass
				if not self.temp: self.file_cache.Lock.release()
				import json
				if metadata:
					metadata = json.loads(metadata)
					if 'utime' in metadata: self.utime = metadata['utime']
					if 'metadata' in metadata: self.metadata = metadata['metadata']
					return True
			return False

	def __singleton_init__(self, path, max_age=0, max_size=0, max_count=0):
		self.path = path
		self.max_age = max_age
		self.max_size = max_size
		self.max_count = max_count
		self._purge_thread = None
		self._add_lock = RLock()
		self._add_seq = 0
		super(FileCache, self).__singleton_init__(path, max_age, max_size, max_count)

	def __new__(cls, path, max_age=0, max_size=0, max_count=0):
		ret = None
		if path:
			try:
				os.makedirs(path, exist_ok=True)
			except Exception as e:
				ret = e
			if os.path.isdir(path):
				ret = super(FileCache, cls).__new__(cls)
		return ret

	@property
	def keys(self):
		content = self._dircontent()
		ret = []
		for f in content:
			if storage_utils.file_extension(f, to_lower=True) == FileCache.OBJ_EXTENSION:
				if (storage_utils.remove_file_extension(f) + '.' + FileCache.METADATA_EXTENSION) in content:
					ret.append(storage_utils.file_name(f, remove_extension=True))
		return ret

	@property
	def files(self):
		content = self._dircontent()
		ret = []
		for f in content:
			if storage_utils.file_extension(f, to_lower=True) == FileCache.OBJ_EXTENSION:
				if (storage_utils.remove_file_extension(f) + '.' + FileCache.METADATA_EXTENSION) in content:
					ret.append(os.path.join(self.path, f))
		return ret

	@property
	def items(self):
		for k in self.keys:
			item = FileCache.Item(self, key=k)
			if item.load_metadata():
				yield item

	@property
	def count(self):
		return len(self.keys)

	@property
	def size(self):
		size = 0
		for f in self._diriterator():
			try:
				size += f.stat().st_size
			except:
				pass
		return size

	def add(self, source, on_finish=None):
		def h(wait):
			if source and source.key:
				ret = False
				item = FileCache.Item(self, key=source.key, metadata=source.metadata)
				item.remove()
				try:
					if source.exists:
						import shutil
						item_tmp = FileCache.Item(self, key=source.key, metadata=source.metadata, temp=True)
						item_tmp.remove()
						shutil.copy2(source.file, item_tmp.obj_file)
						ret = item_tmp.save_metadata()
				except:
					item_tmp.remove()
					wait.set_value(False)
					raise
				if ret:
					self.Lock.acquire()
					item.remove()
					try:
						os.rename(item_tmp.obj_file, item.obj_file)
						os.rename(item_tmp.metadata_file, item.metadata_file)
					except:
						ret = False
						item.remove()
						raise
					finally:
						self.Lock.release()
						wait.set_value(ret)
						item_tmp.remove()
				else:
					wait.set_value(False)
					item_tmp.remove()
		return Thread(target=h, name='FileCache.add', on_finish=on_finish).start()

	def get(self, key):
		ret = None
		if key:
			self.Lock.acquire()
			ret = FileCache.Item(self, key=key)
			if ret.load_metadata():
				#update utime
				AsyncCall(ret.save_metadata)
			else:
				ret = None
			self.Lock.release()
		return ret

	def delete(self, key):
		ret = False
		if key:
			self.Lock.acquire()
			item = FileCache.Item(self, key=key)
			ret = item.exists
			item.remove()
			self.Lock.release()
		return ret

	def clear(self, on_finish=None):
		def h(wait):
			self.Lock.acquire()
			try:
				os.rename(self.path, self.path + '.remove')
				os.makedirs(self.path, exist_ok=True)
			except:
				pass
			it = self._diriterator()
			for f in it:
				if wait.must_terminate(): break
				try:
					os.remove(f.path)
				except:
					pass
			self._purge_thread = None
			self.Lock.release()
			if not wait.must_terminate():
				it = self._diriterator(self.path + '.remove')
				for f in it:
					if wait.must_terminate(): break
					try:
						os.remove(f.path)
					except:
						pass
				try:
					os.rmdir(self.path + '.remove')
				except:
					pass
		self.Lock.acquire()
		if self._purge_thread:
			self._purge_thread.terminate()
			self.Lock.release()
			self._purge_thread.wait()
			self.Lock.acquire()
		self._purge_thread = Thread(target=h, name='FileCache.clear', on_finish=on_finish).start()
		self.Lock.release()

	def purge(self, when=0, on_finish=None):
		def h(wait):
			if when > 0: wait.must_terminate(when)
			min_utime = time.time() - self.max_age
			if not wait.must_terminate():
				self.Lock.acquire()
				orphans = self._orphans()
				self.Lock.release()
				for f in orphans:
					if wait.must_terminate(timeout=0.1): break
					self.Lock.acquire()
					try:
						os.remove(os.path.join(self.path, f))
					except:
						pass
					self.Lock.release()
				if (self.max_age > 0 or self.max_size > 0 or self.max_count > 0) and not wait.must_terminate():
					size = 0
					count = 0
					removed = set()
					remaining = dict()
					for f in self._diriterator():
						if wait.must_terminate(): break
						ext = storage_utils.file_extension(f.name, to_lower=True)
						key = storage_utils.file_name(f.name, remove_extension=True).lower()
						if ext == FileCache.METADATA_EXTENSION:
							try:
								stat = f.stat()
								if self.max_age > 0 and stat.st_mtime < min_utime:
									item = FileCache.Item(self, key=key)
									item.remove()
									if self.max_size > 0: removed.add(key)
									if (self.max_size > 0 or self.max_count > 0) and (key in remaining): del remaining[key]
								elif self.max_size > 0 or self.max_count > 0:
									if key in remaining:
										item = remaining[key]
									else:
										item = FileCache.Item(self, key=key)
										remaining[key] = item
									item.utime = stat.st_mtime
									count += 1
							except:
								pass
						elif self.max_size > 0 and ext == FileCache.OBJ_EXTENSION and (key not in removed):
							try:
								stat = f.stat()
								if key in remaining:
									item = remaining[key]
								else:
									item = FileCache.Item(self, key=key)
									remaining[key] = item
								item._size = stat.st_size
								size += stat.st_size
							except:
								pass
					del removed
					if ((self.max_size > 0 and size > self.max_size) or (self.max_count > 0 and count > self.max_count)) and not wait.must_terminate():
						remaining = sorted(remaining.values(), key=lambda item: item.utime)
						for item in remaining:
							if wait.must_terminate(): break
							item.remove()
							count -= 1
							if self.max_count > 0 and count > self.max_count: continue
							if self.max_size > 0:
								size -= item.size
								if size > self.max_size: continue
							break
			self.Lock.acquire()
			self._purge_thread = None
			self.Lock.release()
		self.Lock.acquire()
		if self._purge_thread:
			self._purge_thread.terminate()
			self.Lock.release()
			self._purge_thread.wait()
			self.Lock.acquire()
		self._purge_thread = Thread(target=h, name='FileCache.purge', on_finish=on_finish).start()
		self.Lock.release()

	def _dircontent(self):
		ret = set()
		self.Lock.acquire()
		for f in self._diriterator():
			ret.add(f.name)
		self.Lock.release()
		return ret

	def _diriterator(self, parent=None):
		if not parent: parent = self.path
		try:
			obj = os.scandir(parent)
		except:
			obj = None
		if obj:
			for o in obj:
				yield o
			obj.close()
		else:
			try:
				list = os.listdir(parent)
			except:
				list = []
			class wrap:
				def __init__(self, parent, f):
					self.parent = parent
					self.name = f
				@property
				def path(self):
					return os.path.join(self.parent, self.name)
				def stat(self):
					return os.stat(self.path)
				def is_file(self):
					return os.path.isfile(self.path)
				def is_dir(self):
					return os.path.isdir(self.path)
			for f in list:
				yield wrap(parent, f)

	def _orphans(self):
		content = self._dircontent()
		ret = []
		for f in content:
			key = storage_utils.remove_file_extension(f) + '.'
			ext = storage_utils.file_extension(f, to_lower=True)
			if ext == FileCache.OBJ_EXTENSION and not (key + FileCache.METADATA_EXTENSION) in content:
				ret.append(f)
			elif ext == FileCache.METADATA_EXTENSION and not (key + FileCache.OBJ_EXTENSION) in content:
				ret.append(f)
		return ret