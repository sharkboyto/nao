#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-25
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os

class CompressedFolder:
	def __new__(cls, path):
		ret = None
		if path:
			from . import storage_utils
			components = storage_utils.reverse_split_component(path)
			relative = []
			for component in list(components):
				if storage_utils.file_extension(component, to_lower=True) == 'zip': break
				relative.append(component)
				components.remove(component)
			zip_file = storage_utils.reverse_join_component(components)
			if zip_file:
				zip = None
				try:
					from zipfile import ZipFile, is_zipfile
					if os.path.isfile(zip_file) and is_zipfile(zip_file):
						zip = ZipFile(zip_file, 'r')
						if zip:
							relative = storage_utils.reverse_join_component(relative).replace('\\', '/')
							try:
								info = zip.getinfo(relative)
							except:
								info = None
							if not info:
								relative = relative.replace('/', '\\')
								try:
									info = zip.getinfo(relative)
								except:
									info = None
							if info:
								ret = super(CompressedFolder, cls).__new__(cls)
								ret.zip = zip
								ret.zip_file = zip_file
								ret.file_info = info
								zip = None
				except:
					ret = None
				finally:
					if zip: zip.close()
		return ret

	def __init__(self, path):
		self.tmp_directory = None
		pass

	def __del__(self):
		self.close()

	@property
	def compressed_filename(self):
		return self.file_info.filename

	def extract(self, path):
		ret = None
		if self.zip and path:
			tmp = self.extract_to_temp()
			if tmp:
				from . import storage_utils
				if os.path.isdir(path): path = os.path.join(path, storage_utils.file_name(tmp))
				try:
					os.remove(path)
				except:
					pass
				try:
					import shutil
					shutil.move(tmp, path)
					ret = path
				except:
					pass
			self.tmp_directory = None
		return ret

	def extract_to_temp(self):
		path = None
		if self.zip:
			try:
				from tempfile import TemporaryDirectory
				self.tmp_directory = TemporaryDirectory()
				self.zip.extract(self.file_info, path=self.tmp_directory.name)
				path = os.path.abspath(os.path.join(self.tmp_directory.name, self.compressed_filename))
				if not os.path.isfile(path) and not os.path.isdir(path): path = None
			except:
				path = None
		if not path: self.tmp_directory = None
		return path

	def close(self):
		self.tmp_directory = None
		if self.zip:
			self.zip.close()
			self.zip = None