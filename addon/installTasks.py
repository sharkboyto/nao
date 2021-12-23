#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import addonHandler

_N = _
addonHandler.initTranslation()

class donate:
	def open():
		import languageHandler
		import webbrowser
		lang = languageHandler.getLanguage()
		if lang:
			lang = lang.split("_")[0].lower()
		else:
			lang = 'en'
		webbrowser.open("https://nvda-nao.org/donate?lang={lang}".format(lang=lang))

	def request():
		import wx
		import gui
		
		# Translators: The title of the dialog requesting donations from users.
		title = _N("Please Donate")
		
		# Translators: The text of the donate dialog
		message = _("""{name} - free add-on for NVDA.
You can make a donation to our team for helping further development of this add-on.
Do you want to make a donation now? For transaction you will be redirected to the website of the developer.""")
		
		name = addonHandler.getCodeAddon().manifest['summary']
		if gui.messageBox(message.format(name=name), title, style=wx.YES_NO|wx.ICON_QUESTION) == wx.YES:
			donate.open()
			return True
		return False

def onInstall():
	donate.request()