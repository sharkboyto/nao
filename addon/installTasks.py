
import webbrowser
import wx
import gui
import addonHandler
from languageHandler import getLanguage
from versionInfo import version_year, version_major

addonHandler.initTranslation()

lang = getLanguage().split("_")[0]
if lang != "en" and lang != "it": lang = "en"

donations_url = "http://nvda-nao.org/{lang}/donation.php".format(lang=lang)

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

	# Translators: The text of the dialog shown during add-on installation.
	message = _(""" {name} - this free add-on for NVDA.
You can make a donation to our team for helping further development of this add-on.
Do you want to make a donation now? For transaction you will be redirected to the website of the developer.""").format(name=manifest['summary'])

	if gui.messageBox(message, _("Request donations for {name}").format(name=manifest['summary']), style=wx.YES_NO|wx.ICON_QUESTION) == wx.YES:
		webbrowser.open(donations_url)
