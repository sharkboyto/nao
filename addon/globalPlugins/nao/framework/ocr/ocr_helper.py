#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-04-23
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import wx
import addonHandler
from logHandler import log
from .. speech import speech
from .. import language
from .. threading import ProgramTerminateEvent, AsyncCall

language.initTranslation()

class OCRHelper:
	PROGRESS_TIMEOUT = 1
	ACTIVATE_LOGS = False
	LOG_NAME = addonHandler.getCodeAddon().manifest['name']

	class FileInCompressedFolder:
		def __init__(self, compressed_folder, file, original_source_file):
			self.compressed_folder = compressed_folder
			self.file = file
			self.original_source_file = original_source_file

	class WaitEvent:
		def __init__(self, timeout=None):
			self.event = ProgramTerminateEvent()
			self.timeout = timeout

		def set(self):
			self.event.set()

		def clear(self):
			self.event.clear()

		def wait(self, timeout=-1):
			if timeout < 0: timeout = self.timeout
			self.event.wait(timeout=timeout)

		def must_terminate(self):
			return self.event.is_global_set()

	def _log(message, *args):
		if OCRHelper.ACTIVATE_LOGS: log.info("{name}: {message}".format(name=OCRHelper.LOG_NAME, message=message), *args)

	def recognize_screenshot(current_window=False):
		from .ocr import OCR
		def recognize_start():
			# Translators: Reporting when recognition (e.g. OCR) begins.
			message = _N("Recognizing")
			if current_window:
				import api
				obj = api.getForegroundObject()
				if obj: message = message + ' ' + obj.name
			speech.queue_message(message)
		OCRHelper._log("Recognizing screenshot")
		OCR.recognize_screenshot(on_start=recognize_start, current_window=current_window)

	def __init__(self, ocr_document_file_extension=None, ocr_document_file_cache=None, speak_errors=True):
		self.supported_extensions = ["pdf", "bmp", "pnm", "pbm", "pgm", "png", "jpg", "jp2", "gif", "tif", "jfif", "jpeg", "tiff", "spix", "webp", "djvu"]
		self.ocr_document_file_extension = ocr_document_file_extension
		self.ocr_document_file_cache = ocr_document_file_cache
		self.speak_errors = speak_errors
		if ocr_document_file_extension: self.supported_extensions.append(ocr_document_file_extension.lower())

	def recognize_file(self, source_file):
		from .uwp_ocr_service import UwpOCRService
		from .ocr_document import OCRDocument
		from .ocr_document_dialog import OCRDocumentDialog
		from .. generic.announce import Announce
		
		def cant_process(source_file):
			# Translators: Reported when unable to process a file for recognition.
			OCRHelper._error_message_box(_("Error, the file could not be processed"), False)
			if source_file:
				OCRHelper._log("Unable to process file %s", source_file)
			else:
				OCRHelper._log("Source file is None or empty")
		
		if not source_file:
			cant_process(None)
			return False
		
		compressed_folder = None
		original_source_file = source_file
		
		if isinstance(source_file, OCRHelper.FileInCompressedFolder):
			compressed_folder = source_file.compressed_folder
			original_source_file = source_file.original_source_file
			source_file = source_file.file
		
		file_extension = None
		if source_file:
			from .. storage import storage_utils
			# Getting the extension to check if is a supported file type.
			file_extension = storage_utils.file_extension(source_file, to_lower=True)
			if not file_extension or not (file_extension in self.supported_extensions):
				# Translators: Reported when the file format is not supported for recognition.
				OCRHelper._error_message_box(_("File not supported"), self.speak_errors)
				OCRHelper._log("File not supported %s", original_source_file)
				return False
		
		if not UwpOCRService.is_uwp_ocr_available():
			# Translators: Reported when Windows OCR is not available.
			OCRHelper._error_message_box(_N("Windows OCR not available"), self.speak_errors)
			OCRHelper._log("Windows OCR not available")
			return False
		
		if not source_file or not os.path.isfile(source_file):
			if compressed_folder:
				cant_process(original_source_file)
				return False
			from .. storage.zip import CompressedFolder
			#check if is a compressed folder
			compressed_folder = CompressedFolder(source_file)
			if compressed_folder:
				announce = Announce()
				def h():
					OCRHelper._log("Deflating %s from %s", compressed_folder.compressed_filename, compressed_folder.zip_file)
					source_file = compressed_folder.extract_to_temp()
					announce.stop()
					if source_file:
						OCRHelper._log("%s from %s extracted to %s", compressed_folder.compressed_filename, compressed_folder.zip_file, source_file)
						wx.CallAfter(self.recognize_file, OCRHelper.FileInCompressedFolder(compressed_folder, source_file, original_source_file))
					else:
						OCRHelper._log("Failed deflating %s from %s", compressed_folder.compressed_filename, compressed_folder.zip_file)
						cant_process(original_source_file)
				announce.start(first_beep_after=0.1, use_text=True, first_text_after=0.1)
				AsyncCall(h)
				return True
		
		if self.ocr_document_file_extension and file_extension == self.ocr_document_file_extension.lower():
			doc = OCRDocument()
			announce = Announce()
			def err():
				# Translators: Reported when the file format is not supported for recognition.
				OCRHelper._error_message_box(_("File not supported"), self.speak_errors)
				OCRHelper._log("File not supported %s", original_source_file)
			def h(result):
				announce.stop()
				if compressed_folder: compressed_folder.close()	#this is for keeping the compressed folder until the end of the async load
				if result.Value and result.Value.document:
					document = result.Value.document
					cached_item = None
					if self.ocr_document_file_cache and document.Source and document.Source.Hash:
						cached_item = self.ocr_document_file_cache.get(document.Source.Hash)
						if cached_item and cached_item.metadata and 'document_source' in cached_item.metadata:
							from .ocr_source import OCRSource
							cached_source = OCRSource.from_dictionary(cached_item.metadata['document_source'])
							#we don't rely only on hash, we check the match also between the sources
							if not cached_source or not cached_source.match_with(document.Source):
								cached_item = None
						else:
							cached_item = None
						if not cached_item: document.async_save_to_cache(self.ocr_document_file_cache)
					OCRHelper._log("Opening document %s", original_source_file)
					wx.CallAfter(OCRDocumentDialog, document=document, ocr_document_file_extension=self.ocr_document_file_extension, cached_item=cached_item, ocr_document_file_cache=self.ocr_document_file_cache)
				else:
					err()
			# Translators: Reported while loading a document.
			announce.start(first_beep_after=0.1, text=_N("Loading document..."), use_text=True, first_text_after=0.1)
			if doc.async_load(source_file, on_finish=h): return True
			announce.stop()
			err()
			return False
		
		OCRHelper._log("Recognizing %s", original_source_file)
		class Control:
			def __init__(self, source_file, original_source_file, compressed_folder, ocr_document_file_extension, ocr_document_file_cache):
				from .ocr import OCR, OCRMultipageSourceFile
				from .ocr_source import UWPOCRSource
				from .ocr_document import OCRDocumentComposer
				from threading import Lock
				
				self.source_file = source_file
				self.original_source_file = original_source_file
				self.compressed_folder = compressed_folder
				self.ocr_document_file_extension = ocr_document_file_extension
				self.ocr_document_file_cache = ocr_document_file_cache
				self.lock = Lock()
				self.announce = Announce()
				self.converter = None
				self.ocr = OCR()
				self.language = UwpOCRService.uwp_ocr_config_language()
				self.document_composer = OCRDocumentComposer()
				self.progress = None
				self.use_progress = False
				self.process_finished = False
				self.wait_event = None
				self.cancelled_event = ProgramTerminateEvent()
				
				if file_extension == 'pdf':
					from .. converters.pdf_converter import PDFConverter
					self.converter = PDFConverter()
					self.use_progress = True
				elif file_extension == 'webp':
					from .. converters.webp_converter import WebpConverter
					self.converter = WebpConverter()
				elif file_extension == 'djvu':
					from .. converters.djvu_converter import DjVuConverter
					self.converter = DjVuConverter()
					self.use_progress = True
				elif OCRMultipageSourceFile.is_multipage_extension(file_extension):
					self.use_progress = True
				
				if self.ocr_document_file_cache: self.wait_event = OCRHelper.WaitEvent(timeout=5)
				
				self.document_composer.Source = UWPOCRSource(file=self.source_file, original_file=self.original_source_file, language=self.language, converter_version=self.converter.version if self.converter else None, on_source_file_hash_finish=self.on_source_file_hash_finish)

			def convert_and_recognize(self):
				if self.use_progress:
					from .ocr_progress import OCRProgressDialog
					# Translators: Reporting when recognition (e.g. OCR) begins.
					self.progress = OCRProgressDialog(title=_N("Recognizing") + ' ' + os.path.basename(self.original_source_file), on_cancel=self.on_cancel)
				else:
					# Translators: Reported when the recognition starts.
					speech.message(_("Process started"))
					self.announce.start()
				
				def proceed():
					if self.converter:
						OCRHelper._log("Using converter %s for %s", self.converter.version, self.original_source_file)
						self.converter.convert(self.source_file, on_finish=self.on_convert_finish, on_progress=self.on_convert_progress, progress_timeout=OCRHelper.PROGRESS_TIMEOUT)
					else:
						self.ocr.recognize_files(source_file, [source_file], document_composer=self.document_composer, language=self.language, on_start=self.on_recognize_start, on_finish=self.on_recognize_finish, on_progress=self.on_recognize_progress, progress_timeout=OCRHelper.PROGRESS_TIMEOUT)
				
				if self.wait_event:
					def h(async_wait):
						self.announce.start()
						self.wait_event.wait()
						self.announce.stop()
						self.lock.acquire()
						if not self.process_finished and not self.cancelled_event.is_set() and not self.wait_event.must_terminate():
							wx.CallAfter(proceed)
						elif self.progress:
							wx.CallAfter(self.progress.Close)
						self.lock.release()
					AsyncCall(h)
				else:
					wx.CallAfter(proceed)

			def on_cancel(self):
				self.cancelled_event.set()
				if self.converter: self.converter.abort()
				self.ocr.abort()
				self.document_composer.Document.close()
				if self.wait_event: self.wait_event.set()
				OCRHelper._log("Processing of %s cancelled", self.original_source_file)

			def on_convert_progress(self, converter, current, total):
				if self.cancelled_event.is_set():
					OCRHelper._log("Abort conversion for %s", self.original_source_file)
					converter.abort()
				if self.progress and current > 0: self.progress.tick(int(round(current / 2)), total, use_percentage=False)

			def on_convert_finish(self, success, aborted, converter):
				if success:
					OCRHelper._log("Conversion of %s done", self.original_source_file)
					self.ocr.recognize_files(converter.source_file, converter.results, document_composer=self.document_composer, language=self.language, on_start=self.on_recognize_start, on_finish=self.on_recognize_finish, on_finish_arg=self.converter, on_progress=self.on_recognize_progress, progress_timeout=OCRHelper.PROGRESS_TIMEOUT)
				else:
					if self.progress: wx.CallAfter(self.progress.Close)
					self.announce.stop()
					if aborted:
						OCRHelper._log("Conversion of %s aborted", self.original_source_file)
					else:
						OCRHelper._log("Error during conversion of %s", self.original_source_file)
						# Translators: Reported when unable to process a file for recognition.
						OCRHelper._error_message_box(_("Error, the file could not be processed"), False)

			def on_recognize_start(self, source_file):
				if not self.use_progress:
					# Translators: Reporting when recognition (e.g. OCR) begins.
					speech.queue_message(_N("Recognizing"))
				OCRHelper._log("OCR recognize started for %s", self.original_source_file)

			def on_recognize_progress(self, current, total):
				if self.cancelled_event.is_set():
					self.ocr.abort()
					OCRHelper._log("Abort OCR recognition of %s", self.original_source_file)
				if self.progress and current > 0:
					if self.converter:
						self.progress.tick(int(round((total + current) / 2)), total, use_percentage=False)
					else:
						self.progress.tick(current, total, use_percentage=False)

			def on_recognize_finish(self, source_file, document, arg=None):
				self.announce.stop()
				if self.progress: self.progress.Close()
				if document:
					if isinstance(document, Exception):
						OCRHelper._log("OCR recognize error for %s: %s", self.original_source_file, str(document))
					else:
						OCRHelper._log("OCR recognize finished for %s", self.original_source_file)
						self.lock.acquire()
						speech.cancel()
						if not self.process_finished:
							self.process_finished = True
							if self.ocr_document_file_cache: document.async_save_to_cache(self.ocr_document_file_cache)
							OCRHelper._log("Opening document %s", self.original_source_file)
							# Translators: The title of the document used to present the result of content recognition.
							OCRDocumentDialog(document=document, title=_N("Result"), ocr_document_file_extension=self.ocr_document_file_extension, ocr_document_file_cache=self.ocr_document_file_cache)
						self.lock.release()

			def on_source_file_hash_finish(self, source, status):
				if self.ocr_document_file_cache:
					if status:
						self.lock.acquire()
						if self.process_finished or self.cancelled_event.is_set():
							self.lock.release()
							return
						cached_item = self.ocr_document_file_cache.get(source.Hash)
						if cached_item and cached_item.metadata and 'document_source' in cached_item.metadata:
							from .ocr_source import OCRSource
							cached_source = OCRSource.from_dictionary(cached_item.metadata['document_source'])
							#we don't rely only on hash, we check the match also between the sources
							if cached_source and cached_source.match_with(source):
								OCRHelper._log("Document %s found in cache with id %s", self.original_source_file, cached_item.key)
								document = OCRDocument()
								def h(result):
									if result.Value and result.Value.document:
										if not self.cancelled_event.is_set():
											self.process_finished = True
											#cancel the recognition and open the cached version
											self.on_cancel()
											# Translators: The title of the document used to present the result of content recognition.
											wx.CallAfter(OCRDocumentDialog, document=result.Value.document, title=_N("Result"), ocr_document_file_extension=self.ocr_document_file_extension, cached_item=cached_item, ocr_document_file_cache=self.ocr_document_file_cache)
											OCRHelper._log("Opening cached document for %s", self.original_source_file)
									else:
										OCRHelper._log("Async load failed %s", cached_item.obj_file)
									self.lock.release()
									if self.wait_event: self.wait_event.set()
								if document.async_load(cached_item.obj_file, on_finish=h): return
								OCRHelper._log("Can't async load %s", cached_item.obj_file)
						self.lock.release()
					else:
						OCRHelper._log("Failed obtaining file hash for %s", self.original_source_file)
				if self.wait_event: self.wait_event.set()
		
		ctrl = Control(source_file=source_file, original_source_file=original_source_file, compressed_folder=compressed_folder, ocr_document_file_extension=self.ocr_document_file_extension, ocr_document_file_cache=self.ocr_document_file_cache)
		ctrl.convert_and_recognize()
		return True

	def _error_message_box(msg, speak_errors):
		if msg:
			if speak_errors:
				speech.queue_message(msg)
			else:
				def h():
					import gui
					gui.mainFrame.prePopup()
					gui.messageBox(
						msg,
						# Translators: The title of an error message dialog.
						OCRHelper.LOG_NAME + ' - ' + _N("Error"),
						wx.OK | wx.ICON_ERROR)
					gui.mainFrame.postPopup()
				wx.CallAfter(h)