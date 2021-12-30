#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-29
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

def merge(a, b, path=None):
	if path is None: path = []
	for key in b:
		if key in a:
			if isinstance(a[key], dict) and isinstance(b[key], dict):
				merge(a[key], b[key], path + [str(key)])
			else:
				a[key] = b[key]
		else:
			a[key] = b[key]
	return a