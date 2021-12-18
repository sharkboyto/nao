#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-17
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
_framework_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "nao_lib"))

def begin_framework_imports():
	import sys
	if _framework_path not in sys.path: sys.path.append(_framework_path)

def end_framework_imports():
	import sys
	if _framework_path in sys.path: sys.path.remove(_framework_path)
