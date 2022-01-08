#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-08
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import api
import os
import queueHandler
import cursorManager
from collections import namedtuple
from .. speech import speech
from .. generic import window
from .. import language

language.initTranslation()

class OCRResult:
	def __init__(self, source_file=None):
		self.source_file = source_file
		#: pages/lines/words data structure
		self.pages = []
		self._length = 0

	def append_page(self, result):
		# result is a LinesWordsResult
		page = { 'start': self._length }
		length = 0
		lines = []
		for line_result in result.data:
			first_word = True
			line = { 'start': length }
			words = []
			for word in line_result:
				if first_word:
					first_word = False
				else:
					# Separate with a space.
					length += 1
				word['offset'] = length
				words.append(word)
				length += len(word["text"])
			# End with new line.
			length += 1
			line['end'] = length
			line['words'] = words
			lines.append(line)
		self._length += length
		page['end'] = self._length
		page['lines'] = lines
		self.pages.append(page)

	def page_at_position(self, pos):
		ret = 0
		for page in self.pages:
			ret += 1
			if pos >= page['start'] and pos < page['end']:
				break
		if ret > self.Pages: ret = self.Pages
		return ret

	def info_at_position(self, pos):
		ret_page = 0
		ret_line = 0
		ret_line_in_page = 0
		last_page_lines = 0
		for page in self.pages:
			ret_page += 1
			page_start = page['start']
			if pos >= page_start and pos < page['end']:
				for line in page['lines']:
					ret_line_in_page +=1
					ret_line += 1
					if pos >= line['start'] + page_start and pos < line['end'] + page_start:
						break
				break
			last_page_lines = len(page['lines'])
			ret_line += last_page_lines
		else:
			if ret_line > 0:
				ret_line += 1
				ret_line_in_page = last_page_lines + 1
		if ret_page > self.Pages: ret_page = self.Pages
		return namedtuple('Info', ['page', 'line', 'line_in_page'])(page=ret_page, line=ret_line, line_in_page=ret_line_in_page)

	def position_at_page(self, page):
		if page < 1: page = 1
		if page >= self.Pages: page = self.Pages
		if page > 0:
			return self.pages[page - 1]['start'], self.pages[page - 1]['end']
		return 0

	def save(self, filename, extra=None):
		if filename:
			try:
				with open(filename, "w", encoding="UTF-8") as f:
					f.write(self.to_json(extra))
				return True
			except Exception as e:
				if os.path.isfile(filename):
					try:
						os.remove(filename)
					except:
						pass
				raise
		return False

	def load(self, filename, validator=None):
		with open(filename, "r", encoding="UTF-8") as f:
			return self.from_json(f.read(), validator)

	def to_json(self, extra=None):
		import json
		if extra:
			data = extra.copy()
		else:
			data = {}
		data.update({
			'source_file': self.source_file,
			'length': self._length,
			'pages': self.pages
		})
		return json.dumps(data)

	def from_json(self, json, validator=None):
		import json as jsonp
		data = jsonp.loads(json)
		if validator:
			if not validator(self, data): return False
		if not 'pages' in data: return False
		self.pages = data['pages']
		self._length = data['length'] if 'length' in data else 0
		self.source_file = data['source_file'] if 'source_file' in data else None
		try:
			self.Text
		except:
			return False
		return True

	@property
	def Json(self):
		return self.to_json()

	@property
	def Length(self):
		if self._length == 0:
			self.Text
		return self._length

	@property
	def Pages(self):
		return len(self.pages)

	@property
	def Text(self):
		text = ""
		for page in self.pages:
			for line in page['lines']:
				first_word = True
				for word in line['words']:
					if first_word:
						first_word = False
					else:
						# Separate with a space.
						text += " "
					text += word["text"]
				# End with new line.
				text += "\n"
		self._length = len(text)
		return text

class MoveToDialog(wx.Dialog):
	def __init__(self, parent, cb):
		self.cb = cb
		# Translators: The title of the dialog used to move to a different page
		super(MoveToDialog, self).__init__(parent, title=_("Move to"))
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# Translators: Identifies a page.
		self.page_field = sHelper.addLabeledControl(_N("page"), wx.TextCtrl)
		
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.CentreOnScreen()
		self.page_field.SetFocus()

	def onOk(self, evt):
		if self.cb:
			try:
				page = int(self.page_field.GetValue())
			except:
				page = None
			wx.CallLater(100, self.cb, page=page)
		self.Destroy()

	def onCancel(self, evt):
		if self.cb:
			wx.CallLater(100, self.cb, page=None)
		self.Destroy()

class OCRResultDialog(wx.Frame):
	def __init__(self, result):
		self.source_file = os.path.basename(result.source_file) if result.source_file else ''
		self.file_path = os.path.dirname(result.source_file) if result.source_file else ''
		self.result = result
		self.text = result.Text if result else ''
		pages = result.Pages if result else 0
		# Translators: The title of the document used to present the result of content recognition.
		title = _N("Result")
		if self.source_file:
			title += ' ' + self.source_file
		title += ' - ' + str(pages) + ' '
		if pages == 1:
			# Translators: In the title of the document used to present the result of content recognition it is the singular "page" used to say "1 page"
			title += _N("page")
		else:
			# Translators: In the title of the document used to present the result of content recognition it is the plural "pages" used to say for example "100 pages"
			title += _N("&Pages").replace('&', '')
		super(OCRResultDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
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
		
		if self.text:
			self.outputCtrl.AppendText(self.text)
			self.outputCtrl.SetInsertionPoint(0)
		
		self.Maximize()
		self.Show()
		window.bring_wx_to_top(self)
		self.outputCtrl.SetFocus()

	def onClose(self, evt):
		self.Destroy()

	def onOutputKeyDown(self, evt):
		key = evt.GetKeyCode()
		if key == wx.WXK_ESCAPE:
			# ESC
			self.Close()
		elif key == wx.WXK_PAGEUP or key == wx.WXK_NUMPAD_PAGEUP:
			# PAGE UP
			self.on_page_move(offset=-1)
		elif key == wx.WXK_PAGEDOWN or key == wx.WXK_NUMPAD_PAGEDOWN:
			# PAGE DOWN
			self.on_page_move(offset=1)
		elif key == wx.WXK_F3:
			# F3 or Shift+F3
			self.find_next(evt.shiftDown)
		elif evt.UnicodeKey == ord(u'F'):
			# Control+F
			speech.suppress_typed_characters()
			wx.CallAfter(self.open_find_dialog)
		elif evt.UnicodeKey == ord(u'P'):
			# P
			speech.suppress_typed_characters()
			self.speak_page(queue=True)
		elif evt.UnicodeKey == ord(u'L'):
			speech.suppress_typed_characters()
			if evt.shiftDown:
				# Shift+L
				self.speak_line(in_page=False, queue=True)
			else:
				# L
				self.speak_line(queue=True)
		elif evt.UnicodeKey == ord(u'C'):
			# C
			speech.suppress_typed_characters()
			if evt.controlDown:
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.outputCtrl.GetStringSelection(), True)
			elif self.text:
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.text, True)
		elif evt.UnicodeKey == ord(u'S'):
			# S
			speech.suppress_typed_characters()
			wx.CallAfter(self.save_as)
		elif evt.UnicodeKey == ord(u'G'):
			# G
			speech.suppress_typed_characters()
			wx.CallAfter(self.move_to)
		else:
			evt.Skip()

	def get_current_page(self):
		if not self.result: return 0
		return self.result.page_at_position(self.outputCtrl.GetInsertionPoint())

	def get_current_line(self):
		if not self.result: return 0
		return self.result.info_at_position(self.outputCtrl.GetInsertionPoint()).line

	def get_current_line_in_page(self):
		if not self.result: return 0
		return self.result.info_at_position(self.outputCtrl.GetInsertionPoint()).line_in_page

	def speak_page(self, page=None, queue=False):
		if page is None:
			page = self.get_current_page()
		# Translators: Indicates the page number in a document.
		speech.message(_N("page %s")%page, queue=queue)

	def speak_line(self, line=None, in_page=True, queue=False):
		if line is None:
			if in_page:
				line = self.get_current_line_in_page()
			else:
				line = self.get_current_line()
		# Translators: Indicates the line number of the text.
		speech.message(_N("line %s")%line, queue=queue)

	def on_page_move(self, page=None, offset=None):
		if self.result:
			if page is None and offset is not None:
				page = self.get_current_page() + offset
			if page is not None:
				if page > self.result.Pages:
					self.outputCtrl.SetInsertionPoint(self.result.position_at_page(page)[1])
					self.speak_page()
					self.speak_line()
					# Translators: a message reported when cursor is at the last line of result window.
					speech.message(_N("Bottom"))
				else:
					self.outputCtrl.SetInsertionPoint(self.result.position_at_page(page)[0])
					self.speak_page()

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
					f.write(self.text)
			except (IOError, OSError) as e:
				# Translators: Dialog text presented when NVDA cannot save a result file.
				message = _("Error saving file: %s") % e.strerror
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_as(self):
		filename = os.path.splitext(self.source_file)[0] + '.txt'
		# Translators: Label of a save dialog
		filename = wx.FileSelector(_N("Save As"), default_path=self.file_path, default_filename=filename, flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, parent=self)
		self.save(filename)

	def move_to(self):
		def h(page):
			speech.cancel()
			if page is None:
				self.speak_page()
			else:
				self.on_page_move(page=page)
		gui.mainFrame.prePopup()
		MoveToDialog(self, h).ShowModal()
		gui.mainFrame.postPopup()

	def doFindText(self, text, reverse=False, caseSensitive=False, willSayAllResume=False):
		speech.cancel()
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
				self._casefold_text = self.text.casefold()
			if reverse:
				pos = self._casefold_text.rfind(casefold_text, 0, pos + len(casefold_text))
			else:
				pos = self._casefold_text.find(casefold_text, pos)
		elif reverse:
			pos = self.text.rfind(text, 0, pos + len(text))
		else:
			pos = self.text.find(text, pos)
		if pos >= 0:
			self._lastFindPos = pos
			min_words = len(text.split())
			if min_words < 5:
				min_words = 5 # speak max 5 words
			current_page = self.get_current_page()
			self.outputCtrl.SetInsertionPoint(pos)
			find_pos_info = self.result.info_at_position(pos)
			if current_page != find_pos_info.page:
				self.speak_page(page=find_pos_info.page,queue=True)
			self.speak_line(line=find_pos_info.line_in_page,queue=True)
			page = self.result.pages[find_pos_info.page - 1]
			line_end = page['lines'][find_pos_info.line_in_page - 1]['end'] + page['start']
			line = self.text[pos:line_end]
			line = line.split()[:min_words]
			line = ' '.join(line)
			speech.queue_message(line)
		else:
			wx.CallAfter(gui.messageBox,_N('text "%s" not found')%text,_N("Find Error"),wx.OK|wx.ICON_ERROR)
		self._lastFindText = text
		self._lastCaseSensitivity = caseSensitive