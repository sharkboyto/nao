#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-07
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import subprocess
from .base.converter import Converter

class DjVuConverter(Converter):
	def __init__(self, clear_on_destruct=True):
		super(DjVuConverter, self).__init__("tmp_djvu", clear_on_destruct)
		self._to_tiff_tool = os.path.join(self._addon_path, "tools", "djvu", "ddjvu.exe")
		self._info_tool = os.path.join(self._addon_path, "tools", "djvu", "djvused.exe")
		self._djvu_pages = False

	def convert(self, djvu_file, on_finish=None, on_progress=None, progress_timeout=1):
		self._djvu_pages = False
		self._convert(djvu_file, "tiff", on_finish, on_progress, progress_timeout)

	@property
	def count(self):
		return self._djvu_pages

	def _command(self, type):
		return "\"{}\" -skip -eachpage -format=tiff -quality=deflate \"{}\" \"{}-%06d.tiff\"".format(self._to_tiff_tool, self.source_file, os.path.join(self.temp_path, self.instance_id))

	def _thread(self):
		self._fetch_info()
		if self._djvu_pages == False:
			self._failed = True
		super(DjVuConverter, self)._thread()

	def _fetch_info(self):
		# The next two lines are to prevent the cmd from being displayed.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		
		cmd = "\"{}\" -e n \"{}\"".format(self._info_tool, self.source_file)
		try:
			p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=si, encoding="unicode_escape", text=True)
			stdout, stderr = p.communicate()
			if p.returncode == 0 and stdout:
				try:
					self._djvu_pages = int(stdout)
				except:
					self._djvu_pages = False
			else:
				self._djvu_pages = False
		except:
			self._djvu_pages = False

DjVuConverter().clear_all()