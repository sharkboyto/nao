#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2026-10-01
#Copyright (C) 2026 Alessandro Cyrille Bougot

import os
import tempfile
import api
from logHandler import log

CONTROL_ID_ATTACHMENTS = 4306

class OutlookHelper:
	def is_outlook(obj=None):
		if obj is None: obj = api.getForegroundObject()
		return obj and obj.appModule and obj.appModule.appName and obj.appModule.appName == 'outlook'

	def __init__(self, obj=None):
		self.obj = obj
		self.nativeOm = None
		if OutlookHelper.is_outlook(obj):
			self.nativeOm = obj.appModule.nativeOm

	def is_valid(self):
		return self.nativeOm != None

	def is_active(self):
		return self.handle and self.handle == ctypes.windll.user32.GetForegroundWindow()

	def getAttachmentsListFromFocus(self):
		"""If the focus is in attachments list, return the attachments list.
		None is returned if the focus is not in attachments list.
		"""

		for o in reversed(api.getFocusAncestors()):
			if getattr(o, 'windowControlID') == CONTROL_ID_ATTACHMENTS:
				return o
		return None

	@staticmethod
	def _logAttachmentMAPIProperties(attachment):
		mapiProperties = {
			"PR_ATTACH_FILENAME": "http://schemas.microsoft.com/mapi/proptag/0x3704001E",
			"PR_ATTACH_LONG_FILENAME": "http://schemas.microsoft.com/mapi/proptag/0x3707001E",
			"PR_DISPLAY_NAME": "http://schemas.microsoft.com/mapi/proptag/0x3001001E",
			"PR_ATTACH_METHOD": "http://schemas.microsoft.com/mapi/proptag/0x37050003",
			"PR_ATTACH_NUM": "http://schemas.microsoft.com/mapi/proptag/0x0E210003",
			"PR_RENDERING_POSITION": "http://schemas.microsoft.com/mapi/proptag/0x370B0003",
			"PR_ATTACH_CONTENT_ID": "http://schemas.microsoft.com/mapi/proptag/0x3712001E",
			"PR_ATTACH_CONTENT_LOCATION": "http://schemas.microsoft.com/mapi/proptag/0x3713001E",
			"PR_ATTACH_FLAGS": "http://schemas.microsoft.com/mapi/proptag/0x37140003",
			"PR_ATTACHMENT_HIDDEN": "http://schemas.microsoft.com/mapi/proptag/0x7FFE000B",
		}
	
		propertyAccessor = attachment.PropertyAccessor
	
		loggedInfos = ["Attachment MAPI properties:"]
		for propertyName, propertyTag in mapiProperties.items():
			try:
				value = propertyAccessor.GetProperty(propertyTag)
			except Exception as e:
				value = f"<error: {e}>"
			loggedInfos.append(f"{propertyName} = {value!r}")
		log.debug("\n".join(loggedInfos))

	def indexOfAttachment(self, obj):
		for idx, o in enumerate(obj.parent.children):
			if obj == o:
				return idx
		raise LookupError('Unable to find index of current item')

	def getAttachmentForIndex(self, attachments, index):
		"""Get attachment for a 0-based defined index in the attachments list.
		This function filters from the list the attachments which are not in the attachments pane.
		"""

		# Increase index by 1 to use it with 1-based index in the COM attachments list.
		index = index + 1
	
		nAtt = 0
		for iAtt in range(1, attachments.Count + 1):
			attachment = attachments.Item(iAtt)
			if self.isAttachmentNotInList(attachment):
				continue
			nAtt += 1
			log.debug(f"Attachment {nAtt} = {attachment.FileName}")
			if nAtt == index:
				return attachment
		raise LookupError("Attachment not found")

	@staticmethod
	def isAttachmentNotInList(attachment):
		isHidden = attachment.PropertyAccessor.GetProperty(
			"http://schemas.microsoft.com/mapi/proptag/0x7FFE000B"
		)
		if isHidden:
			log.debug(f"{attachment.FileName} is hidden")
			return True
		return False

	def currentFileWithPath(self):
		obj = api.getFocusObject()
		attacmentsList = self.getAttachmentsListFromFocus()
		if not attacmentsList:
			log.debug('Not in attachments list')
			return None, None
		index = self.indexOfAttachment(obj)
		inspector = self.nativeOm.ActiveInspector()
		tempDir = ''
		if inspector is not None:
			tempDir = tempfile.mkdtemp()
			mailItem = inspector.CurrentItem
			if mailItem.Attachments.Count > 0:
				[self._logAttachmentMAPIProperties(mailItem.Attachments(na)) for na in range(1, mailItem.Attachments.count + 1)]
				attachment = self.getAttachmentForIndex(mailItem.Attachments, index)
				tempPath = os.path.join(tempDir, attachment.FileName)
				attachment.SaveAsFile(tempPath)
				log.debug(f"tempPath={tempPath}")
				return tempPath, tempDir
		return None, None
