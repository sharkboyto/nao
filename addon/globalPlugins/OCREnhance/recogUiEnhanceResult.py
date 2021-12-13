#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-11-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import ui
#from contentRecog import recogUi
from scriptHandler import willSayAllResume
import speech
import controlTypes
import textInfos

import wx
import gui
import eventHandler
import api

import cursorManager
import NVDAObjects.window
import NVDAObjects.IAccessible
import browseMode
import winUser
import ctypes

class RecogUiEnhanceResultDialog(wx.Dialog):
	def __init__(self, title, result=None, pages_offset=None):
		self.coming_from = api.getFocusObject()
		super(RecogUiEnhanceResultDialog, self).__init__(None, title=title)
		
		self._nvdaobj = None
		self.result = result
		self.pages_offset = pages_offset
		self.resObj = None
		
		self._timer_activate = wx.PyTimer(self.on_timer_activate)
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		text = wx.StaticText(self, label=title)
		text.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
		
		#close_btn = wx.Button(self, wx.ID_CLOSE, label=_("Close"))
		
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		mainSizer.Add(text, border=20, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
		mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		#mainSizer.Add(close_btn, border=20, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
		#mainSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		
		#close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.coming_from.setFocus())
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_keypress)
		self.Bind(wx.EVT_ACTIVATE, self.on_activate)
		self.EscapeId = wx.ID_CLOSE
		
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		
		text.SetLabel('')
		self.Show()

	def on_close(self, evt):
		self._timer_activate.Stop()
		self.DestroyChildren()
		self.Destroy()
		self.resObj = None
		self.coming_from.setFocus()

	def on_result_closed(self):
		self.on_close(None)

	def on_keypress(self, evt: wx.KeyEvent):
		key = evt.GetKeyCode()
		if evt.UnicodeKey == ord(u'A'):
			self.on_activate(None)
		elif evt.UnicodeKey == ord(u'R') and evt.controlDown and evt.shiftDown:
			print(key)
		else:
			evt.Skip()
		#if key == wx.WXK_ESCAPE:
		#	self.Destroy()

	def on_activate(self, evt):
		if evt and evt.GetActive():
			self._timer_activate.Start(100)
		"""oldSpeechMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.off)
		speech.setSpeechMode(oldSpeechMode)
		"""
		#eventHandler.queueEvent("gainFocus", self.resObj)
		#evt.Skip()
		
	def on_timer_activate(self):
		self._timer_activate.Stop()
		if not self._nvdaobj:
			self._nvdaobj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(self.GetHandle(), winUser.OBJID_CLIENT, 0)
		if not self.resObj:
				self.resObj = RecogUiEnhanceResultNVDAObject(parent=self._nvdaobj,result=self.result,pages_offset=self.pages_offset,owner_dlg=self)
				self.result = None
				self.pages_offset = None
		self.resObj.setFocus()

class RecogResultNVDAObject(cursorManager.CursorManager, NVDAObjects.window.Window):
	"""Fake NVDAObject used to present a recognition result in a cursor manager.
	This allows the user to read the result with cursor keys, etc.
	Pressing enter will activate (e.g. click) the text at the cursor.
	Pressing escape dismisses the recognition result.
	"""

	role = controlTypes.Role.DOCUMENT
	# Translators: The title of the document used to present the result of content recognition.
	name = _("Result")
	treeInterceptor = None

	def __init__(self, parent=None, result=None, obj=None, owner_dlg=None):
		if not parent:
			parent = api.getDesktopObject()
		self.parent = parent
		self.result = result
		self.owner_dlg = owner_dlg
		self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
		super(RecogResultNVDAObject, self).__init__(windowHandle=parent.windowHandle)

	def makeTextInfo(self, position):
		# Maintain our own fake selection/caret.
		if position == textInfos.POSITION_SELECTION:
			ti = self._selection.copy()
		elif position == textInfos.POSITION_CARET:
			ti = self._selection.copy()
			ti.collapse()
		else:
			ti = self.result.makeTextInfo(self, position)
		return ti

	def setFocus(self):
		ti = self.parent.treeInterceptor
		if isinstance(ti, browseMode.BrowseModeDocumentTreeInterceptor):
			# Normally, when entering browse mode from a descendant (e.g. dialog),
			# we want the cursor to move to the focus (#3145).
			# However, we don't want this for recognition results, as these aren't focusable.
			ti._enteringFromOutside = True
		# This might get called from a background thread and all NVDA events must run in the main thread.
		eventHandler.queueEvent("gainFocus", self)

	def script_activatePosition(self, gesture):
		try:
			self._selection.activate()
		except NotImplementedError:
			log.debugWarning("Result TextInfo does not implement activate")
	# Translators: Describes a command.
	script_activatePosition.__doc__ = _("Activates the text at the cursor if possible")

	def script_exit(self, gesture):
		if self.owner_dlg:
			self.owner_dlg.on_result_closed()
		else:
			eventHandler.executeEvent("gainFocus", self.parent)
	# Translators: Describes a command.
	script_exit.__doc__ = _("Dismiss the recognition result")

	# The find commands are tricky to support because they pop up dialogs.
	# This moves the focus, so we lose our fake focus.
	# See https://github.com/nvaccess/nvda/pull/7361#issuecomment-314698991
	def script_find(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findNext(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findPrevious(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	__gestures = {
		"kb:enter": "activatePosition",
		"kb:space": "activatePosition",
		"kb:escape": "exit",
	}

class RecogUiEnhanceResultPageOffset():
	def __init__(self, start, length):
		self.start = start
		self.end = start + length

class RecogUiEnhanceResultNVDAObject(RecogResultNVDAObject):
	def __init__(self, parent=None, result=None, obj=None, pages_offset=None, owner_dlg=None):
		super(RecogUiEnhanceResultNVDAObject, self).__init__(parent=parent, result=result, obj=obj, owner_dlg=owner_dlg)
		self.pages_offset = pages_offset

	def script_moveByPage_back(self,gesture):
		self.move_by_page(gesture,-1)

	def script_moveByPage_forward(self,gesture):
		self.move_by_page(gesture,1)

	def script_page_number(self,gesture):
		ui.message(_("page") + " " + str(self.get_current_page() + 1))

	def move_by_page(self,gesture,direction):
		page = self.get_current_page() + direction
		if page >= 0 and page < len(self.pages_offset):
			ui.message(_("page") + " " + str(page + 1))
			offset = self.pages_offset[page].start - self._selection._startOffset
			self._caretMovementScriptHelper(gesture,textInfos.UNIT_CHARACTER,offset,extraDetail=True,handleSymbols=True,speak=False)
			self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,extraDetail=True,handleSymbols=True)

	def get_current_page(self):
		i = 0
		for offset in self.pages_offset:
			if self._selection._startOffset >= offset.start and self._selection._startOffset < offset.end:
				return i
			i = i + 1
		return 0

	def _caretMovementScriptHelper(self,gesture,unit,direction=None,posConstant=textInfos.POSITION_SELECTION,posUnit=None,posUnitEnd=False,extraDetail=False,handleSymbols=False,speak=True):
		oldInfo=self.makeTextInfo(posConstant)
		info=oldInfo.copy()
		info.collapse(end=self.isTextSelectionAnchoredAtStart)
		if self.isTextSelectionAnchoredAtStart and not oldInfo.isCollapsed:
			info.move(textInfos.UNIT_CHARACTER,-1)
		if posUnit is not None:
			# expand and collapse to ensure that we are aligned with the end of the intended unit
			info.expand(posUnit)
			try:
				info.collapse(end=posUnitEnd)
			except RuntimeError:
				# MS Word has a "virtual linefeed" at the end of the document which can cause RuntimeError to be raised.
				# In this case it can be ignored.
				# See #7009
				pass
			if posUnitEnd:
				info.move(textInfos.UNIT_CHARACTER,-1)
		if direction is not None:
			info.expand(unit)
			info.collapse(end=posUnitEnd)
			if info.move(unit,direction)==0 and isinstance(self,textInfos.DocumentWithPageTurns):
				try:
					self.turnPage(previous=direction<0)
				except RuntimeError:
					pass
				else:
					info=self.makeTextInfo(textInfos.POSITION_FIRST if direction>0 else textInfos.POSITION_LAST)
		# #10343: Speak before setting selection because setting selection might
		# move the focus, which might mutate the document, potentially invalidating
		# info if it is offset-based.
		selection = info.copy()
		info.expand(unit)
		if speak:
			if not willSayAllResume(gesture):
				speech.speakTextInfo(info, unit=unit, reason=controlTypes.OutputReason.CARET)
			if not oldInfo.isCollapsed:
				speech.speakSelectionChange(oldInfo, selection)
		self.selection = selection

	__gestures = {
		"kb:NVDA+Shift+p": "page_number",
	}