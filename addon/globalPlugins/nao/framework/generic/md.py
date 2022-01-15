#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-14
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
from struct import pack

class MessageDigest:
	def __new__(cls, hash='sha1'):
		ret = None
		if hash:
			try:
				import hashlib
				ret = super(MessageDigest, cls).__new__(cls)
				if hash == 'sha1': ret.md = hashlib.sha1()
				elif hash == 'sha224': ret.md = hashlib.sha224()
				elif hash == 'sha256': ret.md = hashlib.sha256()
				elif hash == 'sha384': ret.md = hashlib.sha384()
				elif hash == 'sha512': ret.md = hashlib.sha512()
				else: ret = None
			except:
				ret = None
		return ret

	def __init__(self, hash='sha1'):
		if not hash: self.md = None

	def digest(self):
		return self.md.digest()
	def hexdigest(self):
		return self.md.hexdigest()

	def update_bytes(self, value):
		self.md.update(value)
		return self

	def update_string(self, *args):
		for s in args:
			if s is None:
				self.update_char(0)
			else:
				self.update_bytes(s.encode('utf-8'))
		return self

	def update_char(self, *args):
		return self.update_bytes(pack('%db' %len(args), *args))
	def update_unsigned_char(self, *args):
		return self.update_bytes(pack('%dB' %len(args), *args))
	def update_short(self, *args):
		return self.update_bytes(pack('%dh' %len(args), *args))
	def update_unsigned_short(self, *args):
		return self.update_bytes(pack('%dH' %len(args), *args))
	def update_int(self, *args):
		return self.update_bytes(pack('%di' %len(args), *args))
	def update_unsigned_int(self, *args):
		return self.update_bytes(pack('%dI' %len(args), *args))
	def update_long(self, *args):
		return self.update_bytes(pack('%dl' %len(args), *args))
	def update_unsigned_long(self, *args):
		return self.update_bytes(pack('%dL' %len(args), *args))
	def update_long_long(self, *args):
		return self.update_bytes(pack('%dq' %len(args), *args))
	def update_unsigned_long_long(self, *args):
		return self.update_bytes(pack('%dQ' %len(args), *args))

	def update_float(self, *args):
		return self.update_bytes(pack('%df' %len(args), *args))
	def update_double(self, *args):
		return self.update_bytes(pack('%dd' %len(args), *args))

	def update_file(self, filename):
		with open(filename, 'rb') as f:
			b = f.read(32768)
			while b:
				self.update_bytes(b)
				b = f.read(32768)
		return self

	def update_file_async(self, filename, callback=None):
		from .. threading import Thread
		class T(Thread):
			def __init__(self, md):
				super(T, self).__init__()
				self.md = md

			def proc(self, wait):
				result = {
					'filename': filename,
					'status': False,
					'md': self.md
				}
				try:
					with open(filename, 'rb') as f:
						b = f.read(32768)
						while b:
							self.md.update_bytes(b)
							if wait.must_terminate():
								wait.terminated(value=result)
								return
							b = f.read(32768)
					result['status'] = True
				except Exception as e:
					result['status'] = e
				if callback: callback(result)
				wait.terminated(value=result)
		thread = T(self)
		thread.start()
		return thread.AsyncResult