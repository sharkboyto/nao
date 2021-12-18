#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-18
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import addonHandler

addonHandler.initTranslation()

def open():
	import languageHandler
	import webbrowser
	lang = languageHandler.getLanguage()
	if lang:
		lang = lang.split("_")[0].lower()
	else:
		lang = 'en'
	webbrowser.open("https://nvda-nao.org/donate?{lang}".format(lang=lang))

def request():
	import wx
	import gui
	
	# Translators: The title of the donate dialog
	title = _("Request donations for {name}")
	
	# Translators: The text of the donate dialog
	message = _(""" {name} - this free add-on for NVDA.
You can make a donation to our team for helping further development of this add-on.
Do you want to make a donation now? For transaction you will be redirected to the website of the developer.""")
	
	name = addonHandler.getCodeAddon().manifest['summary']
	if gui.messageBox(message.format(name=name), title.format(name=name), style=wx.YES_NO|wx.ICON_QUESTION) == wx.YES:
		open()
		return True
	return False