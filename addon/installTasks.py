#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-18
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import addonHandler
from versionInfo import version_year, version_major

import os
import sys

_framework_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "nao_lib"))
if _framework_path not in sys.path: sys.path.append(_framework_path)
from nao import donate
if _framework_path in sys.path: sys.path.remove(_framework_path)

addonHandler.initTranslation()

def onInstall():
	manifest = addonHandler.getCodeAddon().manifest
	try:
		if isinstance(manifest["minimumNVDAVersion"], unicode):
			minVersion = manifest["minimumNVDAVersion"].split(".")
		else:
			minVersion = manifest["minimumNVDAVersion"]
	except NameError:
		minVersion = manifest["minimumNVDAVersion"]
	
	year = int(minVersion[0])
	major = int(minVersion[1])
	
	if (version_year, version_major) < (year, major):
		gui.messageBox(_("This version of NVDA is incompatible. To install the add-on, NVDA version {year}.{major} or higher is required. Please update NVDA.").format(year=year, major=major), _("Error"), style=wx.OK | wx.ICON_ERROR)
		raise RuntimeError("Incompatible NVDA version")
	
	donate.request()