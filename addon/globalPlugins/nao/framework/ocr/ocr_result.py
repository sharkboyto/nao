#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-09
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import api
import os
import numbers
import queueHandler
import cursorManager
from collections import namedtuple
from .. speech import speech
from .. generic import window
from .. import language

language.initTranslation()

class OCRResult:
	OCRRESULT_JSON_TYPE = 'ocr_result'
	OCRRESULT_JSON_VERSION = 1

	def __new__(cls, filename=None, validator=None, source_file=None):
		ret = super(OCRResult, cls).__new__(cls)
		if filename:
			try:
				if not ret.load(filename, validator=validator):
					ret = None
			except Exception as e:
				ret = e
		return ret

	def __init__(self, filename=None, validator=None, source_file=None):
		if not filename:
			self.clear()
			self.source_file = source_file

	def clear(self):
		self.source_file = None
		self._length = 0
		self._hash = None
		#: pages/lines/words data structure
		self.pages = []

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
		if length == 0:
			# Empty page, end with new line.
			length = 1
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

	def save(self, filename, extra=None, compress=True):
		if filename:
			import gzip
			try:
				json = self.to_json(extra)
				json_gz = None
				if compress:
					try:
						json_gz = gzip.compress(json.encode("UTF-8"))
					except:
						json_gz = None
				if json_gz:
					with open(filename, "wb") as f:
						f.write(json_gz)
				else:
					with open(filename, "w", encoding="UTF-8") as f:
						f.write(json)
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
		ret = False
		if filename:
			import gzip
			try:
				with gzip.open(filename, mode='rt', encoding="UTF-8") as f:
					ret = self.from_json(f.read(), validator)
			except:
				if os.path.isfile(filename):
					try:
						with open(filename, "r", encoding="UTF-8") as f:
							ret = self.from_json(f.read(), validator)
					except:
						raise
				else:
					raise
		if not ret:
			self.clear()
		return ret

	def to_json(self, extra=None):
		import json
		if extra:
			data = extra.copy()
		else:
			data = {}
		data.update({
			'version': OCRResult.OCRRESULT_JSON_VERSION,
			'type': OCRResult.OCRRESULT_JSON_TYPE,
			'source_file': self.source_file,
			'length': self._length,
			'pages': self.pages
		})
		hash = self.Hash
		if hash:
			data['hash'] = hash.hex()
		return json.dumps(data)

	def from_json(self, json, validator=None):
		import json as jsonp
		self.clear()
		data = jsonp.loads(json)
		if validator:
			if not validator(self, data): return False
		if not 'type' in data or data['type'] != OCRResult.OCRRESULT_JSON_TYPE: return False
		if not 'pages' in data: return False
		self.pages = data['pages']
		self._length = data['length'] if 'length' in data else 0
		self.source_file = data['source_file'] if 'source_file' in data else None
		try:
			self.Text
		except:
			self.clear()
			return False
		return True

	def get_page(self, page):
		if isinstance(page, numbers.Number):
			if page > 0 and page <= self.Pages:
				page = self.pages[page - 1]
			else:
				page = None
		return page

	def get_line(self, line, page):
		if isinstance(line, numbers.Number):
			page = self.get_page(page)
			if page and line > 0 and line <= len(page['lines']):
				line = page['lines'][line - 1]
			else:
				line = None
		return line

	def get_line_text(self, line, page=None):
		text = ""
		line = self.get_line(line, page)
		if line:
			first_word = True
			for word in line['words']:
				if first_word:
					first_word = False
				else:
					# Separate with a space.
					text += " "
				text += word["text"]
		return text

	def get_page_text(self, page):
		text = ""
		page = self.get_page(page)
		if page:
			for line in page['lines']:
				text += self.get_line_text(line)
				# End with new line.
				text += "\n"
		return text

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
			if len(page['lines']) > 0:
				text += self.get_page_text(page)
			else:
				# Empty page, end with new line.
				text += "\n"
		self._length = len(text)
		return text

	@property
	def Hash(self):
		if not self._hash:
			try:
				import hashlib
				from struct import pack
				md = hashlib.sha256()
				md.update(pack('<ll', len(self.pages), self.Length))
				for page in self.pages:
					md.update(pack('<lll', page['start'], page['end'], len(page['lines'])))
					for line in page['lines']:
						md.update(pack('<lll', line['start'], line['end'], len(line['words'])))
						for word in line['words']:
							md.update(pack('<lllll', word['x'], word['y'], word['width'], word['height'], word['offset']))
							md.update(word['text'].encode('utf-8'))
				self._hash = md.digest()
			except:
				pass
		return self._hash

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
	def __init__(self, result, ocr_result_file_extension=None, pickle=None):
		self.source_file = os.path.basename(result.source_file) if result.source_file else ''
		self.file_path = os.path.dirname(result.source_file) if result.source_file else ''
		self.result = result
		self.text = result.Text if result else ''
		self.ocr_result_file_extension = ocr_result_file_extension
		self.pickle = pickle
		
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
			speech.suppress_typed_characters()
			if evt.controlDown:
				# Control+C
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.outputCtrl.GetStringSelection(), True)
			elif self.text:
				# C
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.text, True)
		elif evt.UnicodeKey == ord(u'S'):
			if evt.shiftDown:
				# Shift+S
				if self.ocr_result_file_extension:
					speech.suppress_typed_characters()
					wx.CallAfter(self.save_result_as)
				else:
					evt.Skip()
			else:
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
					# Translators: a message reported when cursor is at the last line of result window.
					speech.message(_N("Bottom"))
					self.speak_page()
					self.speak_line()
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
		if filename and self.text:
			try:
				with open(filename, "w", encoding="UTF-8") as f:
					f.write(self.text)
			except (IOError, OSError) as e:
				# Translators: Dialog text presented when NVDA cannot save a result file.
				message = _("Error saving file: %s") % e.strerror
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_result(self, filename):
		if filename and self.result and self.result.Length > 0:
			try:
				self.result.save(filename)
			except (IOError, OSError) as e:
				# Translators: Dialog text presented when NVDA cannot save a result file.
				message = _("Error saving file: %s") % e.strerror
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)
			except Exception as e:
				# Translators: Dialog text presented when NVDA cannot save a result file.
				message = _("Error saving file: %s") % str(e)
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_as(self):
		if self.text:
			filename = os.path.splitext(self.source_file)[0] + '.txt'
			# Translators: Label of a save dialog
			with wx.FileDialog(self, _N("Save As"), wildcard="txt (*.txt)|*.txt", defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
				if file_dialog.ShowModal() != wx.ID_CANCEL:
					filename = file_dialog.GetPath()
					self.save(filename)

	def save_result_as(self):
		if self.ocr_result_file_extension and self.result and self.result.Length > 0:
			filename = os.path.splitext(self.source_file)[0] + '.' + self.ocr_result_file_extension
			# Translators: Label of a save dialog
			title = _N("Save As")
			title += ' - ' + self.ocr_result_file_extension
			with wx.FileDialog(self, title, wildcard=self.ocr_result_file_extension + " (*." + self.ocr_result_file_extension + ")|*." + self.ocr_result_file_extension, defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
				if file_dialog.ShowModal() != wx.ID_CANCEL:
					filename = file_dialog.GetPath()
					self.save_result(filename)

	def move_to(self):
		def h(page):
			speech.cancel()
			if page is None:
				self.speak_page()
			else:
				self.on_page_move(page=page)
				# After the dialog closes the cursor is not going to read the line
				speech.queue_message(self.result.get_line_text(page=page, line=1))
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