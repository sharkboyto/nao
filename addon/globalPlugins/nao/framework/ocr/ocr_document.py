#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import numbers
import addonHandler
from threading import Lock
from collections import namedtuple
from .ocr_source import OCRSource
from .. threading import Thread

class OCRDocument:
	default_data = {
		'type': 'ocr_document',
		'version': 1,
		'generator': addonHandler.getCodeAddon().manifest["name"] + '-' + addonHandler.getCodeAddon().manifest["version"],
		'length': 0,
		'hash': None,
	}	

	def __new__(cls, filename=None, validator=None, source=None):
		ret = super(OCRDocument, cls).__new__(cls)
		if filename:
			try:
				if not ret.load(filename, validator=validator):
					ret = None
			except Exception as e:
				ret = e
		return ret

	def __init__(self, filename=None, validator=None, source=None):
		if not filename:
			self.clear()
			self._source = source

	def clear(self):
		self.data = OCRDocument.default_data.copy()
		self.data['pages'] = []	#: pages/lines/words data structure
		self._source = None
		self._hash_result = None
		self._hash_lock = Lock()
		self._text = None

	def append_page(self, result):
		page = {
			'start': self.data['length'],
			'width': result.width,
			'height': result.height
		}
		length = 0
		lines = []
		# result.data is a LinesWordsResult
		for line_result in result.data.data:
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
		self.data['length'] += length
		page['end'] = self.data['length']
		page['lines'] = lines
		self.Pages.append(page)

	def page_at_position(self, pos):
		ret = 0
		for page in self.Pages:
			ret += 1
			if pos >= page['start'] and pos < page['end']:
				break
		if ret > self.PagesCount: ret = self.PagesCount
		return ret

	def info_at_position(self, pos):
		ret_page = 0
		ret_line = 0
		ret_line_in_page = 0
		last_page_lines = 0
		for page in self.Pages:
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
		if ret_page > self.PagesCount: ret_page = self.PagesCount
		return namedtuple('Info', ['page', 'line', 'line_in_page'])(page=ret_page, line=ret_line, line_in_page=ret_line_in_page)

	def position_at_page(self, page):
		if page < 1: page = 1
		if page >= self.PagesCount: page = self.PagesCount
		if page > 0:
			return self.Pages[page - 1]['start'], self.Pages[page - 1]['end']
		return 0

	def save(self, filename, extra=None, compress=True):
		res = self.async_save(filename, extra=extra, compress=compress)
		if res:
			res.wait()
			if res.Exception:
				raise res.Exception
			return res.Value.status
		return False

	def async_save(self, filename, on_finish=None, extra=None, compress=True):
		if filename:
			def h(wait):
				result = {
					'filename': filename,
					'status': False
				}
				try:
					json = self.to_json(extra)
					json_gz = None
					if compress:
						try:
							import gzip
							json_gz = gzip.compress(json.encode("UTF-8"))
						except:
							json_gz = None
					if json_gz:
						with open(filename, "wb") as f:
							f.write(json_gz)
					else:
						with open(filename, "w", encoding="UTF-8") as f:
							f.write(json)
					result['status'] = True
				except:
					if os.path.isfile(filename):
						try:
							os.remove(filename)
						except:
							pass
					raise
				finally:
					wait.set_value_dict(result)
			return Thread(target=h, on_finish=on_finish, name="OCRDocumentSave").start()
		return False

	def load(self, filename, validator=None):
		res = self.async_load(filename, validator=validator)
		if res:
			res.wait()
			if res.Exception:
				raise res.Exception
			return res.Value.status
		return False

	def async_load(self, filename, on_finish=None, validator=None):
		if filename:
			def h(wait):
				result = {
					'filename': filename,
					'status': False,
					'document': None
				}
				try_plain = False
				import gzip
				try:
					with gzip.open(filename, mode='rt', encoding="UTF-8") as f:
						result['status'] = self.from_json(f.read(), validator)
				except:
					if os.path.isfile(filename):
						try_plain = True
					else:
						raise
				finally:
					if not try_plain: wait.set_value_dict(result)
				if try_plain:
					try:
						with open(filename, "r", encoding="UTF-8") as f:
							result['status'] = self.from_json(f.read(), validator)
					except:
						wait.set_value_dict(result)
						raise
				if result['status']:
					result['document'] = self
				else:
					self.clear()
				wait.set_value_dict(result)
			return Thread(target=h, on_finish=on_finish, name="OCRDocumentLoad").start()
		return False

	def to_json(self, extra=None):
		import json
		data = extra.copy() if extra else {}
		if self._source: data['source'] = self._source.dictionary()
		data.update(self.data)
		hash = self.Hash
		if hash:
			data['hash'] = hash.hex()
		elif 'hash' in data:
			del data['hash']
		return json.dumps(data)

	def from_json(self, json, validator=None):
		import json as jsonp
		self.clear()
		data = jsonp.loads(json)
		if validator:
			if not validator(self, data): return False
		if not 'type' in data or data['type'] != OCRDocument.default_data['type']: return False
		if not 'pages' in data: return False
		self.data.update(data)
		if 'hash' in self.data: del self.data['hash']
		if 'source' in self.data:
			self._source = OCRSource.from_dictionary(self.data['source'])
			del self.data['source']
		ret = True
		try:
			self.Text
		except:
			ret = False
			self.clear()
			raise
		if ret:
			self._hash_lock.acquire()
			def h(result):
				self._hash_result = result
				self._hash_lock.release()
			self.async_hash(h)
		return ret

	def get_page(self, page):
		if isinstance(page, numbers.Number):
			if page > 0 and page <= self.PagesCount:
				page = self.Pages[page - 1]
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

	def async_hash(self, on_finish=None):
		def h(wait):
			from .. generic.md import MessageDigest
			md = MessageDigest('sha256')
			if md:
				md.update_long(self.PagesCount, self.TextLength)
				for page in self.Pages:
					if wait.must_terminate(): break
					md.update_long(page['start'], page['end'], len(page['lines']))
					for line in page['lines']:
						md.update_long(line['start'], line['end'], len(line['words']))
						for word in line['words']:
							md.update_long(word['x'], word['y'], word['width'], word['height'], word['offset'])
							md.update_string(word['text'])
				else:
					wait.set_value(md.digest())
		return Thread(target=h, on_finish=on_finish, name="OCRDocumentHash").start()

	@property
	def Source(self):
		return self._source

	@property
	def SourceFile(self):
		return self._source.file if self._source else None

	@property
	def Json(self):
		return self.to_json()

	@property
	def TextLength(self):
		if self.data['length'] == 0:
			self.Text
		return self.data['length']

	@property
	def PagesCount(self):
		return len(self.data['pages'])

	@property
	def Pages(self):
		return self.data['pages']

	@property
	def Text(self):
		if self._text is None:
			self._text = ""
			for page in self.Pages:
				if len(page['lines']) > 0:
					self._text += self.get_page_text(page)
				else:
					# Empty page, end with new line.
					self._text += "\n"
			self.data['length'] = len(self._text)
		return self._text

	@property
	def Hash(self):
		self._hash_lock.acquire()
		if self._hash_result is None:
			self._hash_result = self.async_hash()
			self._hash_result.wait()
		ret = self._hash_result.Value
		self._hash_lock.release()
		return ret