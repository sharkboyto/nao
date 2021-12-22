#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import gui
import wx
import queueHandler
import tones
import config
import time
from .. import language
from .. speech import speech
from .. generic import window

language.initTranslation()

class OCRProgressDialog(wx.Dialog):
	def __init__(self, title, on_cancel=None):
		self._active = False
		self._last_string_value = False
		self._last_percent_value = 0
		self._last_speech = 0
		self._title = title
		
		super(OCRProgressDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
		self._beep_timer = wx.PyTimer(self._on_beep)
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self._gauge = None #wx.Gauge(self)
		
		self._value_text = wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL)
		self._value_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
		
		#mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		#mainSizer.Add(self._gauge, border=20, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		mainSizer.Add(self._value_text, border=200, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		
		def on_close(evt):
			self._active = False
			self._gauge = None
			self._value_text = None
			self._beep_timer.Stop()
			self.Destroy()
			if on_cancel:
				on_cancel()
		
		def on_cancel_button_key_down(evt):
			key = evt.GetKeyCode()
			if key == wx.WXK_RETURN or key == wx.WXK_NUMPAD_ENTER:
				# ENTER
				self.Close()
			evt.skip()
		
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
			button_cancel.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
			self.Bind(wx.EVT_KEY_DOWN, on_cancel_button_key_down)
			def on_focus(evt):
				# keep focus on cancel button
				button_cancel.SetFocus()
			self.Bind(wx.EVT_SET_FOCUS, on_focus)
		
		self.Bind(wx.EVT_CLOSE, on_close)
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
	def last_string_value(self):
		return self._last_string_value

	@property
	def last_percent_value(self):
		return self._last_percent_value

	def on_activate(self, active):
		self._active = active
		if self._active:
			self._last_speech = time.time()
			self._beep_timer.Start(1000)
		else:
			self._beep_timer.Stop()

	def tick(self, current, total, use_percentage=True):
		self._last_percent_value = int(round(100 * current / total))
		if use_percentage:
			self._last_string_value = str(self._last_percent_value) + '%'
		else:
			# Translators: Spoken to indicate progress of a processing that is the number of processed items of a total of items to be processed.
			self._last_string_value = _N("{number} of {total}").format(number=current, total=total)
		if self._gauge:
			def h():
				self._gauge.SetRange(total)
				self._gauge.SetValue(current)
			queueHandler.queueFunction(queueHandler.eventQueue, h)
		self._on_tick()

	def _on_tick(self):
		if self.last_string_value is not False:
			def h():
				if self._value_text:
					self._value_text.SetLabel(self.last_string_value)
					self.SetTitle(self._title + ' ' + self.last_string_value)
				if self.is_active:
					now = time.time()
					if now - self._last_speech >= 5:
						pbConf = config.conf["presentation"]["progressBarUpdates"]
						if pbConf["progressBarOutputMode"] in ("speak","both"):
							speech.message(self.last_string_value)
							self._last_speech = now
			queueHandler.queueFunction(queueHandler.eventQueue, h)

	def _on_beep(self):
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] in ("beep","both"):
			tones.beep(pbConf["beepMinHZ"]*2**(self.last_percent_value/25.0),40)