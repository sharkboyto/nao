#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-24
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import json
import urllib.request
import ssl
import updateCheck

def json_post(url, obj):
	response = False
	if url:
		obj = json.dumps(obj).encode('utf-8')
		req = urllib.request.Request(url)
		req.add_header('Content-Type', 'application/json; charset=utf-8')
		req.add_header('Content-Length', len(obj))
		try:
			response = urllib.request.urlopen(req, obj)
		except IOError as e:
			if isinstance(e.reason, ssl.SSLCertVerificationError) and e.reason.reason == "CERTIFICATE_VERIFY_FAILED":
				# Windows fetches trusted root certificates on demand.
				# Python doesn't trigger this fetch (PythonIssue:20916), so try it ourselves
				updateCheck._updateWindowsRootCertificates()
				# and then retry the update check.
				response = urllib.request.urlopen(req, obj)
			else:
				response = False
	return response