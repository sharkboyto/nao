#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-11-30
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import ui
from contentRecog import recogUi
from scriptHandler import willSayAllResume
import speech
import controlTypes
import textInfos

class RecogUiEnhanceResultPageOffset():
	def __init__(self, start, length):
		self.start = start
		self.end = start + length

class RecogUiEnhanceResultNVDAObject(recogUi.RecogResultNVDAObject):
	def __init__(self, result=None, obj=None, pages_offset=None):
		super(RecogUiEnhanceResultNVDAObject, self).__init__(result, obj)
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