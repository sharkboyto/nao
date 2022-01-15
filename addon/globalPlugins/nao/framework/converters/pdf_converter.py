#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-15
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import subprocess
from .base.converter import Converter

class PDFConverter(Converter):
	def __init__(self, clear_on_destruct=True):
		super(PDFConverter, self).__init__("tmp_pdf", clear_on_destruct)
		self._to_png_tool = os.path.join(self._addon_path, "tools", "pdftopng.exe")
		self._info_tool = os.path.join(self._addon_path, "tools", "pdfinfo.exe")
		self._pdf_pages = False

	def convert(self, pdf_file, on_finish=None, on_progress=None, progress_timeout=1):
		self._pdf_pages = False
		self._convert(pdf_file, "png", on_finish, on_progress, progress_timeout)

	@property
	def count(self):
		return self._pdf_pages

	def _command(self, type):
		return "\"{}\" \"{}\" \"{}\"".format(self._to_png_tool, self.source_file, os.path.join(self.temp_path, self.instance_id))

	def _thread_proc(self, wait):
		self._fetch_info()
		if self._pdf_pages == False:
			self._failed = True
		super(PDFConverter, self)._thread_proc(wait)

	def _fetch_info(self):
		# The next two lines are to prevent the cmd from being displayed.
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		
		cmd = "\"{}\" \"{}\"".format(self._info_tool, self.source_file)
		try:
			p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, startupinfo=si, encoding="unicode_escape", text=True)
			stdout, stderr = p.communicate()
			if p.returncode == 0 and stdout:
				lines = stdout.splitlines()
				try:
					pages = [int(i[6:]) for i in lines if i.lower().startswith('pages:')]
				except:
					pages = [False]
					pass
				finally:
					self._pdf_pages = pages[0]
			else:
				self._pdf_pages = False
		except:
			self._pdf_pages = False

PDFConverter().clear_all()