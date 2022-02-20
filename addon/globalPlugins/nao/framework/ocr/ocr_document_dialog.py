#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-28
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import wx
import gui
import api
import os
import queueHandler
from .. speech import speech
from .. import language

language.initTranslation()

class OCRDocumentMoveToDialog(wx.Dialog):
	def __init__(self, parent, callback, current_page=None, pages_count=None):
		self.callback = callback
		# Translators: The title of the dialog used to move to a different page
		super(OCRDocumentMoveToDialog, self).__init__(parent, title=_("Move to"))
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = gui.guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		
		sHelperH = sHelper.addItem(gui.guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL))
		
		# Translators: Identifies a page.
		self.page_field = sHelperH.addLabeledControl(_N("page"), wx.TextCtrl)
		
		if current_page:
			self.page_field.SetValue(str(current_page))
		
		if pages_count:
			# Translators: Spoken to indicate the current page in a total of pages.
			sHelperH.addItem(wx.StaticText(self, label=_N("{number} of {total}").format(number='', total=pages_count)), flag=wx.ALIGN_CENTER_VERTICAL)
		
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		mainSizer.Add(sHelper.sizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.CentreOnScreen()
		self.page_field.SetFocus()

	def onOk(self, evt):
		if self.callback:
			try:
				page = int(self.page_field.GetValue())
			except:
				page = None
			wx.CallLater(100, self.callback, page=page)
		self.Destroy()

	def onCancel(self, evt):
		if self.callback:
			wx.CallLater(100, self.callback, page=None)
		self.Destroy()

class OCRDocumentDialogSettings:
	def __init__(self):
		self.modified = False
		self._last_position = 0

	def from_dictionary(value):
		ret = OCRDocumentDialogSettings()
		if value:
			if 'last_position' in value: ret._last_position = value['last_position']
		return ret

	def dictionary(self):
		ret = {
			'last_position': self._last_position
		}
		return ret

	@property
	def is_default(self):
		if self._last_position != 0: return False
		return True

	@property
	def last_position(self):
		return self._last_position

	@last_position.setter
	def last_position(self, value):
		if value != self._last_position:
			self._last_position = value
			self.modified = True

class OCRDocumentDialog(wx.Frame):
	def __init__(self, document, title=None, ocr_document_file_extension=None, cached_item=None, ocr_document_file_cache=None):
		from threading import RLock
		from .. generic import window
		
		self.source_file = os.path.basename(document.SourceFile) if document and document.SourceFile else ''
		self.file_path = os.path.dirname(document.SourceFile) if document and document.SourceFile else ''
		self.document = document
		self.ocr_document_file_extension = ocr_document_file_extension
		self.ocr_document_file_cache = ocr_document_file_cache
		
		if self.ocr_document_file_cache and not cached_item and document and document.Source:
			cached_item = self.ocr_document_file_cache.get(document.Source.Hash)
		if cached_item and cached_item.metadata and 'document_dialog' in cached_item.metadata:
			self.document_dialog_settings = OCRDocumentDialogSettings.from_dictionary(cached_item.metadata['document_dialog'])
		else:
			self.document_dialog_settings = OCRDocumentDialogSettings()
		
		pages = document.PagesCount if document else 0
		if not title:
			# Translators: Identifies a document.
			title = _N("document")
		if self.source_file:
			title += ' ' + self.source_file
		title += ' - ' + str(pages) + ' '
		if pages == 1:
			# Translators: In the title of the document used to present the result of content recognition it is the singular "page" used to say "1 page"
			title += _N("page")
		else:
			# Translators: In the title of the document used to present the result of content recognition it is the plural "pages" used to say for example "100 pages"
			title += _N("&Pages").replace('&', '')
		self.title = title
		super(OCRDocumentDialog, self).__init__(gui.mainFrame, wx.ID_ANY, self.title)
		
		self._lastFindText = ""
		self._lastCaseSensitivity = False
		self._lastFindPos = -1
		self._casefold_text = None
		
		self._close_lock = RLock()
		self._async_update_title = None
		
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		self.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		self.outputCtrl.Bind(wx.EVT_LEFT_UP, self.onOutputLeftUp)
		
		self.outputCtrl.AppendText(self.Text)
		self.outputCtrl.SetInsertionPoint(self.document_dialog_settings.last_position)
		if self.document_dialog_settings.last_position > 0: self.onInsertionPointChanged(self.document_dialog_settings.last_position, 0)
		
		self.Maximize()
		self.Show()
		window.bring_wx_to_top(self)
		self.outputCtrl.SetFocus()

	@property
	def Text(self):
		return self.document.Text if self.document else ''

	def onClose(self, evt):
		self._close_lock.acquire()
		if self._async_update_title: self._async_update_title.terminate()
		if self.document:
			if self.ocr_document_file_cache and self.document.Source:
				self.document_dialog_settings.last_position = self.outputCtrl.GetInsertionPoint()
				if self.document_dialog_settings.modified and self.document.Source.Hash:
					#update cached metadata with document_dialog_settings
					cached_item = self.ocr_document_file_cache.get(self.document.Source.Hash)
					if cached_item:
						from .. threading import AsyncCall
						if not cached_item.metadata: cached_item.metadata = {}
						if self.document_dialog_settings.is_default:
							if 'document_dialog' in cached_item.metadata: del cached_item.metadata['document_dialog']
						else:
							cached_item.metadata['document_dialog'] = self.document_dialog_settings.dictionary()
						AsyncCall(cached_item.save_metadata)
			self.document.close()
			self.document = None
		self._close_lock.release()
		self.Destroy()

	def onInsertionPointChanged(self, actual, previous, event=None):
		from .. threading import AsyncCall
		self.document_dialog_settings.last_position = actual
		self._close_lock.acquire()
		if self._async_update_title:
			self._async_update_title.terminate()
			self._async_update_title = None
		if self.document:
			if not event or isinstance(event, wx.MouseEvent):
				self.update_title()
			else:
				self._async_update_title = AsyncCall(self.update_title, async_call_params={'after': 0.5})
		self._close_lock.release()

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
			# F or Control+F
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
			if evt.controlDown:
				# Control+S
				if self.ocr_document_file_extension:
					speech.suppress_typed_characters()
					wx.CallAfter(self.save_document_as)
				else:
					evt.Skip()
			elif not evt.shiftDown:
				# S
				speech.suppress_typed_characters()
				wx.CallAfter(self.save_as)
		elif evt.UnicodeKey == ord(u'G'):
			# G
			speech.suppress_typed_characters()
			wx.CallAfter(self.move_to)
		else:
			self._check_insertion_point_changed(event=evt)
			evt.Skip()

	def onOutputLeftUp(self, evt):
		self._check_insertion_point_changed(event=evt)
		evt.Skip()

	def get_info_at_current_position(self):
		return self.document.info_at_position(self.outputCtrl.GetInsertionPoint()) if self.document else None

	def get_current_page(self):
		return self.document.page_at_position(self.outputCtrl.GetInsertionPoint()) if self.document else 0

	def get_current_line(self):
		info = self.get_info_at_current_position()
		return info.line if info else 0

	def get_current_line_in_page(self):
		info = self.get_info_at_current_position()
		return info.line_in_page if info else 0

	def speak_page(self, page=None, queue=False):
		if page is None: page = self.get_current_page()
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

	def update_title(self):
		self._close_lock.acquire()
		if self.document:
			info = self.document.info_at_position(self.document_dialog_settings.last_position)
			title = self.title
			if info.line > 1:
				# Translators: Presented when a page is the current page
				title += ' - ' + _N("current page") + ' ' + str(info.page) + ' '
				# Translators: Indicates the line number of the text.
				title += _N("line %s")%info.line_in_page
			wx.CallAfter(self.SetTitle, title)
		self._close_lock.release()

	def on_page_move(self, page=None, offset=None):
		if self.document:
			if page is None and offset is not None: page = self.get_current_page() + offset
			if page is not None:
				insertion_point = self.outputCtrl.GetInsertionPoint()
				if page > self.document.PagesCount:
					pos = self.document.position_at_page(page)[1]
					self.outputCtrl.SetInsertionPoint(pos)
					# Translators: a message reported when cursor is at the last line of document window.
					speech.message(_N("Bottom"))
					self.speak_page()
					self.speak_line()
				else:
					pos = self.document.position_at_page(page)[0]
					self.outputCtrl.SetInsertionPoint(pos)
					self.speak_page()
				if insertion_point != pos: self.onInsertionPointChanged(pos, insertion_point)

	def open_find_dialog(self, reverse=False):
		import cursorManager
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
				# Translators: Dialog text presented when NVDA cannot save a document file.
				message = _("Error saving file: %s") % e.strerror
				# Translators: The title of an error message dialog.
				gui.messageBox(message, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_document(self, filename):
		if filename and self.document and self.document.TextLength > 0:
			# Translators: Dialog text presented when NVDA cannot save a document file.
			message = _("Error saving file: %s")
			def h(result):
				if result.Exception:
					# Translators: The title of an error message dialog.
					wx.CallAfter(gui.messageBox, message % str(result.Exception), _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)
			if not self.document.async_save(filename, on_finish=h):
				# Translators: The title of an error message dialog.
				wx.CallAfter(gui.messageBox, message % filename, _N("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def save_as(self):
		if self.Text:
			from .. storage import storage_utils
			filename = storage_utils.file_name(self.source_file, remove_extension=True) + '.txt'
			# Translators: Label of a save dialog
			with wx.FileDialog(self, _N("Save As"), wildcard="txt (*.txt)|*.txt", defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
				if file_dialog.ShowModal() != wx.ID_CANCEL:
					filename = file_dialog.GetPath()
					self.save(filename)

	def save_document_as(self):
		if self.ocr_document_file_extension and self.document and self.document.TextLength > 0:
			from .. storage import storage_utils
			filename = storage_utils.file_name(self.source_file, remove_extension=True) + '.' + self.ocr_document_file_extension
			# Translators: Label of a save dialog
			title = _N("Save As")
			title += ' - ' + self.ocr_document_file_extension
			with wx.FileDialog(self, title, wildcard=self.ocr_document_file_extension + " (*." + self.ocr_document_file_extension + ")|*." + self.ocr_document_file_extension, defaultFile=filename, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
				if file_dialog.ShowModal() != wx.ID_CANCEL:
					filename = file_dialog.GetPath()
					self.save_document(filename)

	def move_to(self):
		def h(page):
			speech.cancel()
			if page is None:
				self.speak_page()
			else:
				self.on_page_move(page=page)
				# After the dialog closes the cursor is not going to read the line
				info = self.get_info_at_current_position()
				if info:
					speech.queue_message(self.document.get_line_text(page=info.page, line=info.line_in_page))
		gui.mainFrame.prePopup()
		OCRDocumentMoveToDialog(self, callback=h, current_page=self.get_current_page(), pages_count=self.document.PagesCount if self.document else None).ShowModal()
		gui.mainFrame.postPopup()

	def doFindText(self, text, reverse=False, caseSensitive=False, willSayAllResume=False):
		speech.cancel()
		pos = insertion_point = self.outputCtrl.GetInsertionPoint()
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
			if min_words < 5: min_words = 5 # speak max 5 words
			current_page = self.get_current_page()
			self.outputCtrl.SetInsertionPoint(pos)
			find_pos_info = self.document.info_at_position(pos)
			if current_page != find_pos_info.page: self.speak_page(page=find_pos_info.page,queue=True)
			self.speak_line(line=find_pos_info.line_in_page,queue=True)
			page = self.document.Pages[find_pos_info.page - 1]
			line_end = page['lines'][find_pos_info.line_in_page - 1]['end'] + page['start']
			line = self.Text[pos:line_end]
			line = line.split()[:min_words]
			line = ' '.join(line)
			speech.queue_message(line)
			if insertion_point != pos: self.onInsertionPointChanged(pos, insertion_point)
		else:
			wx.CallAfter(gui.messageBox,_N('text "%s" not found')%text,_N("Find Error"),wx.OK|wx.ICON_ERROR)
		self._lastFindText = text
		self._lastCaseSensitivity = caseSensitive

	def _check_insertion_point_changed(self, event=None):
		def h():
			pos = self.outputCtrl.GetInsertionPoint()
			if self.document_dialog_settings.last_position != pos:
				self.onInsertionPointChanged(pos, self.document_dialog_settings.last_position, event=event)
		wx.CallAfter(h)