#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-20
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import addonHandler

_builtin_translate = _
addonHandler.initTranslation()

class Language:
	_builtin_set = set()
	_addon_set = set()

	def translate(message):
		if message in Language._builtin_set: return _builtin_translate(message)
		if message in Language._addon_set: return _(message)
		ret = _(message)
		if ret != message:
			Language._addon_set.add(message)
			return ret
		Language._builtin_set.add(message)
		return _builtin_translate(message)

def initTranslation():
	import inspect
	try:
		callerFrame = inspect.currentframe().f_back
		callerFrame.f_globals['_'] = Language.translate
		callerFrame.f_globals['_N'] = _builtin_translate
	finally:
		del callerFrame # Avoid reference problems with frames (per python docs)