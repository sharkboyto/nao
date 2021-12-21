#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-21
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import gui
import wx
import queueHandler
from .. import language
from .. speech import speech
from .. generic import window
from .. generic.beepThread import BeepThread

language.initTranslation()

class OCRProgressDialog(wx.Frame):
	def __init__(self, title, on_cancel=None):
		self._beeper = BeepThread()
		self._active = False
		self._last_value = False
		
		super(OCRProgressDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self._value_text = wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL)
		self._value_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
		
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		mainSizer.Add(self._value_text, border=200, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		
		def on_close(evt):
			self._active = False
			self._value_text = None
			self._beeper.stop()
			self.Destroy()
			if on_cancel:
				on_cancel()
		
		def on_activate(evt):
			self.on_activate(evt.GetActive())
			evt.Skip()
		
		def on_iconize(evt):
			self.on_activate(not evt.IsIconized())
			evt.Skip()
		
		if on_cancel:
			# Translators: A cancel button on a message dialog.
			button_cancel = wx.Button(self, label=_N("Cancel"), id=wx.ID_CLOSE)
			mainSizer.Add(button_cancel, border=200, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
			mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
			button_cancel.Bind(wx.EVT_BUTTON, on_close)
		
		self.Bind(wx.EVT_CLOSE, on_close)
		self.EscapeId = wx.ID_CLOSE
		
		self.Bind(wx.EVT_ACTIVATE, on_activate)
		self.Bind(wx.EVT_ICONIZE, on_iconize)
		
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		self.CentreOnScreen()
		self.Show()
		
		window.bring_wx_to_top(self)
		
		if on_cancel:
			button_cancel.SetFocus()

	@property
	def is_active(self):
		return self._active

	@property
	def last_value(self):
		return self._last_value

	def on_activate(self, active):
		self._active = active
		if self._active:
			self._beeper.start()
			if self.last_value is not False:
				speech.message(self.last_value)
		else:
			self._beeper.stop()

	def tick(self, current, total, use_percentage=True):
		if use_percentage:
			value = str(int(round(100 * current / total))) + '%'
		else:
			# Translators: Spoken to indicate progress of a processing that is the number of processed items of a total of items to be processed.
			value = _N("{number} of {total}").format(number=current, total=total)
		self._last_value = value
		queueHandler.queueFunction(queueHandler.eventQueue, self._on_tick, value)

	def _on_tick(self, value):
		if self._value_text:
			self._value_text.SetLabel(value)
		if self.is_active:
			speech.message(value)