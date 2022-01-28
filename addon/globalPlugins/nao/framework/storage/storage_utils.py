#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-25
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os

def file_extension(file, to_lower=False):
	file_extension = None
	if file:
		file_extension = os.path.splitext(file)[1]
		if file_extension and file_extension.startswith('.'): file_extension = file_extension[1:]
		if to_lower: file_extension = file_extension.lower()
	return file_extension

def remove_file_extension(file):
	return os.path.splitext(file)[0] if file else None

def file_name(file, remove_extension=False):
	if remove_extension:
		return os.path.splitext(os.path.basename(file))[0] if file else None
	return os.path.basename(file) if file else None

def parent_name(file):
	return os.path.dirname(file)

def reverse_split_component(file):
	ret = []
	while file:
		split = os.path.split(file)
		if split[1]:
			ret.append(split[1])
			file = split[0]
		else:
			ret.append(split[0])
			file = None
	return ret

def reverse_join_component(splitted):
	ret = ''
	for c in splitted:
		if ret:
			ret = os.path.join(c, ret)
		else:
			ret = c
	return ret