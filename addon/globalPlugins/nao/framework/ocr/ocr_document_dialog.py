#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-16
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import api
import os
import queueHandler
import cursorManager
from .. speech import speech
from .. generic import window
from .. import language

language.initTranslation()

class OCRDocumentMoveToDialog(wx.Dialog):
	def __init__(self, parent, cb):
		self.cb = cb
		# Translators: The title of the dialog used to move to a different page
		super(OCRDocumentMoveToDialog, self).__init__(parent, title=_("Move to"))
		
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

class OCRDocumentDialog(wx.Frame):
	def __init__(self, result, ocr_document_file_extension=None, pickle=None):
		self.source_file = os.path.basename(result.SourceFile) if result and result.SourceFile else ''
		self.file_path = os.path.dirname(result.SourceFile) if result and result.SourceFile else ''
		self.result = result
		self.ocr_document_file_extension = ocr_document_file_extension
		self.pickle = pickle
		
		pages = result.PagesCount if result else 0
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
		super(OCRDocumentDialog, self).__init__(gui.mainFrame, wx.ID_ANY, title)
		
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
		
		self.outputCtrl.AppendText(self.Text)
		self.outputCtrl.SetInsertionPoint(0)
		
		self.Maximize()
		self.Show()
		window.bring_wx_to_top(self)
		self.outputCtrl.SetFocus()

	@property
	def Text(self):
		return self.result.Text if self.result else ''

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
			elif self.Text:
				# C
				queueHandler.queueFunction(queueHandler.eventQueue, api.copyToClip, self.Text, True)
		elif evt.UnicodeKey == ord(u'S'):
			if evt.shiftDown:
				# Shift+S
				if self.ocr_document_file_extension:
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
				if page > self.result.PagesCount:
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
		if filename and self.Text:
			try:
				with open(filename, "w", encoding="UTF-8") as f:
					f.write(self.Text)
			except (IOError, OSError) as e:
				# Translators: Dialog text presented when NVDA cannot save a result file.
				message = _("Error saving file: %s") % e.strerror
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_result(self, filename):
		if filename and self.result and self.result.TextLength > 0:
			# Translators: Dialog text presented when NVDA cannot save a result file.
			message = _("Error saving file: %s")
			def h(result):
				if result.Exception:
					wx.CallAfter(gui.messageBox, message % str(result.Exception), _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)
			if not self.result.async_save(filename, on_finish=h):
				# Translators: The title of an error message dialog.
				wx.CallAfter(gui.messageBox, message % filename, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_as(self):
		if self.Text:
			filename = os.path.splitext(self.source_file)[0] + '.txt'
			# Translators: Label of a save dialog
			with wx.FileDialog(self, _N("Save As"), wildcard="txt (*.txt)|*.txt", defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
				if file_dialog.ShowModal() != wx.ID_CANCEL:
					filename = file_dialog.GetPath()
					self.save(filename)

	def save_result_as(self):
		if self.ocr_document_file_extension and self.result and self.result.TextLength > 0:
			filename = os.path.splitext(self.source_file)[0] + '.' + self.ocr_document_file_extension
			# Translators: Label of a save dialog
			title = _N("Save As")
			title += ' - ' + self.ocr_document_file_extension
			with wx.FileDialog(self, title, wildcard=self.ocr_document_file_extension + " (*." + self.ocr_document_file_extension + ")|*." + self.ocr_document_file_extension, defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
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
		OCRDocumentMoveToDialog(self, h).ShowModal()
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
				self._casefold_text = self.Text.casefold()
			if reverse:
				pos = self._casefold_text.rfind(casefold_text, 0, pos + len(casefold_text))
			else:
				pos = self._casefold_text.find(casefold_text, pos)
		elif reverse:
			pos = self.Text.rfind(text, 0, pos + len(text))
		else:
			pos = self.Text.find(text, pos)
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
			page = self.result.Pages[find_pos_info.page - 1]
			line_end = page['lines'][find_pos_info.line_in_page - 1]['end'] + page['start']
			line = self.Text[pos:line_end]
			line = line.split()[:min_words]
			line = ' '.join(line)
			speech.queue_message(line)
		else:
			wx.CallAfter(gui.messageBox,_N('text "%s" not found')%text,_N("Find Error"),wx.OK|wx.ICON_ERROR)
		self._lastFindText = text
		self._lastCaseSensitivity = caseSensitive