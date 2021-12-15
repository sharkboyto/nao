#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-15
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import ui
import api
import os
import queueHandler
import speech
import cursorManager
#import webbrowser

class RecogUiEnhanceResultPageOffset():
	def __init__(self, start, length):
		self.start = start
		self.end = start + length

def ui_message(message, queue=False):
	if queue:
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, message)
	else:
		ui.message(message)

class RecogUiEnhanceResultDialog(wx.Frame):
	def __init__(self, result, pages_offset=None, file_name=None):
		self.file_name = os.path.basename(file_name)
		self.file_path = os.path.dirname(file_name)
		self.result = result
		self.pages_offset = pages_offset
		
		title = _("Result") + (' ' + self.file_name if self.file_name else '')
		title = title + ' - ' + str(len(self.pages_offset)) + ' ' + (_("page") if len(self.pages_offset) == 1 else _("&Pages").replace('&', ''))
		super(RecogUiEnhanceResultDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
		self._lastFindText = ""
		self._lastCaseSensitivity = False
		self._lastFindPos = -1
		self._casefold_text = None
		
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
			# ESC
			self.Close()
		elif key == wx.WXK_PAGEUP or key == wx.WXK_NUMPAD_PAGEUP:
			# PAGE UP
			self.on_page_move(-1)
		elif key == wx.WXK_PAGEDOWN or key == wx.WXK_NUMPAD_PAGEDOWN:
			# PAGE DOWN
			self.on_page_move(1)
		elif key == wx.WXK_F3:
			# F3 or Shift+F3
			self.find_next(evt.shiftDown)
		elif evt.UnicodeKey == ord(u'F'):
			# Control+F
			speech._suppressSpeakTypedCharacters(1)
			wx.CallAfter(self.open_find_dialog)
		elif evt.UnicodeKey == ord(u'P'):
			# P
			speech._suppressSpeakTypedCharacters(1)
			self.speak_page(queue=True)
		elif evt.UnicodeKey == ord(u'L'):
			# L
			speech._suppressSpeakTypedCharacters(1)
			self.speak_line(queue=True)
		elif evt.UnicodeKey == ord(u'C'):
			# C
			speech._suppressSpeakTypedCharacters(1)
			if evt.controlDown:
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.outputCtrl.GetStringSelection(), True)
			else:
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.result.text, True)
		elif evt.UnicodeKey == ord(u'S'):
			# S
			speech._suppressSpeakTypedCharacters(1)
			wx.CallAfter(self.save_as)
			"""elif evt.UnicodeKey == ord(u'D'):
				# D
				speech._suppressSpeakTypedCharacters(1)
				webbrowser.open("https://google.com")
			"""
		else:
			evt.Skip()

	def get_current_page(self):
		return self.get_pos_page()

	def get_current_line(self):
		return self.get_pos_line()

	def get_pos_page(self, pos=None):
		if pos is None:
			pos = self.outputCtrl.GetInsertionPoint()
		i = 1
		for offset in self.pages_offset:
			if pos >= offset.start and pos < offset.end:
				break
			i = i + 1
		if i > len(self.pages_offset):
			i = len(self.pages_offset)
		return i

	def get_pos_line(self, pos=None):
		if pos is None:
			pos = self.outputCtrl.GetInsertionPoint()
		i = 0
		for offset in self.result.lines:
			if pos < offset:
				break
			i = i + 1
		return i + 1

	"""def get_line_start_end_offset(self, line):
		if line < 1 or line > len(self.result.lines):
			return False
		if line == 1:
			return [0, self.result.lines[0]]
		return [self.result.lines[line - 2], self.result.lines[line - 1]]
	"""

	def speak_page(self, page=None, queue=False):
		if page is None:
			page = self.get_current_page()
		ui_message(_("page %s")%page, queue)

	def speak_line(self, line=None, queue=False):
		if line is None:
			line = self.get_current_line()
		ui_message(_("line %s")%line, queue)

	def on_page_move(self, offset):
		page = self.get_current_page() + offset
		if page <= 0:
			page = 1
		if page <= len(self.pages_offset):
			self.speak_page(page)
			self.outputCtrl.SetInsertionPoint(self.pages_offset[page - 1].start)

	def open_find_dialog(self, reverse=False):
		gui.mainFrame.prePopup()
		cursorManager.FindDialog(self, self, self._lastFindText, self._lastCaseSensitivity, reverse).ShowModal()
		gui.mainFrame.postPopup()

	def find_next(self, reverse=False):
		if not self._lastFindText:
			self.open_find_dialog(reverse)
		else:
			self.doFindText(self._lastFindText, caseSensitive=self._lastCaseSensitivity, reverse=reverse)

	def save(self, filename):
		if filename:
			try:
				with open(filename, "w", encoding="UTF-8") as f:
					f.write(self.result.text)
			except (IOError, OSError) as e:
				gui.messageBox(_("Error saving log: %s") % e.strerror, _("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_as(self):
		filename = os.path.splitext(self.file_name)[0] + '.txt'
		filename = wx.FileSelector(_("Save As"), default_path=self.file_path, default_filename=filename, flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, parent=self)
		self.save(filename)

	def doFindText(self, text, reverse=False, caseSensitive=False, willSayAllResume=False):
		speech.cancelSpeech()
		pos = self.outputCtrl.GetInsertionPoint()
		if pos == self._lastFindPos:
			if text != self._lastFindText or caseSensitive != self._lastCaseSensitivity:
				self._lastFindPos = -1
			elif reverse:
				pos = pos - len(self._lastFindText)
			else:
				pos = pos + len(self._lastFindText)
		if not caseSensitive:
			casefold_text = text.casefold()
			if self._casefold_text is None:
				self._casefold_text = self.result.text.casefold()
			if reverse:
				pos = self._casefold_text.rfind(casefold_text, 0, pos + len(casefold_text))
			else:
				pos = self._casefold_text.find(casefold_text, pos)
		elif reverse:
			pos = self.result.text.rfind(text, 0, pos + len(text))
		else:
			pos = self.result.text.find(text, pos)
		if pos >= 0:
			self._lastFindPos = pos
			current_page = self.get_current_page()
			find_page = self.get_pos_page(pos)
			self.outputCtrl.SetInsertionPoint(pos)
			min_words = len(text.split())
			if min_words < 5:
				min_words = 5 # speak max 5 words
			line = self.get_pos_line(pos)
			if current_page != find_page:
				self.speak_page(page=find_page,queue=True)
			self.speak_line(line=line,queue=True)
			line_end = self.result.lines[line - 1]
			line = self.result.text[pos:line_end]
			line = line.split()[:min_words]
			line = ' '.join(line)
			ui_message(line, True)
		else:
			wx.CallAfter(gui.messageBox,_('text "%s" not found')%text,_("Find Error"),wx.OK|wx.ICON_ERROR)
		self._lastFindText = text
		self._lastCaseSensitivity = caseSensitive