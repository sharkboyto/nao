#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-24
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

def os_version():
	import sys
	import os
	winVersion = sys.getwindowsversion()
	osVersion = {
		"major": winVersion.major,
		"minor": winVersion.minor,
		"build": winVersion.build,
		"sp": {
			"major": winVersion.service_pack_major,
			"minor": winVersion.service_pack_minor,
		},
		"type": winVersion.product_type,
		"x64": os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64"
	}
	return osVersion

def nvda_version():
	import languageHandler
	import buildVersion
	nvdaVersion = {
		"language": languageHandler.getLanguage()
	}
	try:
		nvdaVersion["year"] = buildVersion.version_year
	except:
		pass
	try:
		nvdaVersion["major"] = buildVersion.version_major
	except:
		pass
	try:
		nvdaVersion["minor"] = buildVersion.version_minor
	except:
		pass
	try:
		nvdaVersion["build"] = buildVersion.version_build
	except:
		pass
	return nvdaVersion

def addon_version():
	import addonHandler
	addonVersion = {
		"name": addonHandler.getCodeAddon().manifest["name"],
		"version": addonHandler.getCodeAddon().manifest["version"],
	}
	return addonVersion

def composed_version():
	version = {
		"addon": addon_version(),
		"os": os_version(),
		"nvda": nvda_version()
	}
	return version