#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-14
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import ui
import queueHandler
import speech

def ui_message(message, queue=False):
	if queue:
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, message)
	else:
		ui.message(message)

class RecogUiEnhanceResultDialog(wx.Frame):
	def __init__(self, result, pages_offset=None, title=None):
		# Translators: The title of the document used to present the result of content recognition.
		title = _("Result") + (' ' + title) if title else ''
		super(RecogUiEnhanceResultDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
		self.result = result
		self.pages_offset = pages_offset
		
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		self.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		
		if self.result and self.result.text:
			self.outputCtrl.AppendText(self.result.text)
			self.outputCtrl.SetInsertionPoint(0)
		self.outputCtrl.SetFocus()
		
		self.Raise()
		self.Maximize()
		self.Show()

	def onClose(self, evt):
		self.Destroy()

	def onOutputKeyDown(self, evt):
		key = evt.GetKeyCode()
		if key == wx.WXK_ESCAPE:
			self.Close()
		elif key == wx.WXK_PAGEUP or key == wx.WXK_NUMPAD_PAGEUP:
			self.on_page_move(-1)
		elif key == wx.WXK_PAGEDOWN or key == wx.WXK_NUMPAD_PAGEDOWN:
			self.on_page_move(1)
		elif evt.UnicodeKey == ord(u'P'):
			speech._suppressSpeakTypedCharacters(1)
			self.speak_page(queue=True)
		elif evt.UnicodeKey == ord(u'L'):
			speech._suppressSpeakTypedCharacters(1)
			self.speak_line(queue=True)
		else:
			evt.Skip()

	def get_current_page(self):
		pos = self.outputCtrl.GetInsertionPoint()
		i = 0
		for offset in self.pages_offset:
			if pos >= offset.start and pos < offset.end:
				return i
			i = i + 1
		return 0

	def get_current_line(self):
		pos = self.outputCtrl.GetInsertionPoint()
		i = 1
		for offset in self.result.lines:
			if pos < offset:
				return i
			i = i + 1
		return 0

	def speak_page(self, page=None, queue=False):
		if page is None:
			page = self.get_current_page() + 1
		ui_message(("page") + " " + str(page), queue)

	def speak_line(self, line=None, queue=False):
		if line is None:
			line = self.get_current_line()
		ui_message(("line") + " " + str(line), queue)

	def on_page_move(self, offset):
		page = self.get_current_page() + offset
		if page >= 0 and page < len(self.pages_offset):
			self.speak_page(page + 1)
			self.outputCtrl.SetInsertionPoint(self.pages_offset[page].start)