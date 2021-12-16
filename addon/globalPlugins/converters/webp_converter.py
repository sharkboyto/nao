#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-16
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
from .base.converter import Converter

class WebpConverter(Converter):
	def __init__(self, clear_on_destruct=True):
		super(WebpConverter, self).__init__("tmp_webp", clear_on_destruct)
		self._to_png_tool = os.path.join(self._addon_path, "tools", "dwebp.exe")

	def to_png(self, webp_file, on_finish=None):
		self._convert(webp_file, "png", on_finish)

	def _command(self, type):
		return "{} \"{}\" -o \"{}.png\"".format(self._to_png_tool, self.source_file, os.path.join(self.temp_path, self.instance_id))
