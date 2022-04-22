#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-04-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

from contentRecog import uwpOcr, recogUi
from .ocr_service import OCRService
from .. threading import ProgramTerminateEvent

class UwpOCRService(OCRService):
	def is_uwp_ocr_available():
		import winVersion
		return winVersion.isUwpOcrAvailable()

	def is_uwp(self):
		return True

	def needs_pixels(self):
		return True

	def recognize(self, item):
		if item.pixels:
			recognizer = uwpOcr.UwpOcr(language=item.language)
			try:
				imgInfo = recogUi.RecogImageInfo.createFromRecognizer(item.x, item.y, item.width, item.height, recognizer)
			except ValueError as e:
				item.on_recognize_result(e)
				return
			event = ProgramTerminateEvent()
			def h(result):
				if not isinstance(result, Exception):
					from collections import namedtuple
					result = {
						'data': result,
						'language': item.language,
						'x': item.x,
						'y': item.y,
						'width': item.width,
						'height': item.height
					}
					result = namedtuple('UwpOCRServiceResult', result)(**result)
				item.on_recognize_result(result)
				event.set()
			try:
				recognizer.recognize(item.pixels, imgInfo, h)
				event.wait()
			except Exception as e:
				item.on_recognize_result(e)
		else:
			item.on_recognize_result(ValueError("pixels not set"))