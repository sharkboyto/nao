#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-25
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
from .base.converter import Converter

class WebpConverter(Converter):
	def __init__(self):
		super(WebpConverter, self).__init__("tmp_webp")
		self._to_png_tool = os.path.join(self._addon_path, "tools", "dwebp.exe")

	def convert(self, webp_file, on_finish=None, on_progress=None, progress_timeout=1):
		self._convert(webp_file, "png", on_finish=on_finish, on_progress=on_progress, progress_timeout=progress_timeout)

	@property
	def version(self):
		return "dwebp 1.0.3"

	@property
	def count(self):
		return 1

	def _command(self, type):
		return "{} \"{}\" -o \"{}.png\"".format(self._to_png_tool, self.source_file, os.path.join(self.temp_path, self.instance_id))

WebpConverter().clear_all()