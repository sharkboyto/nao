#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-04-22
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

def get_size(dc=None):
	if dc is None:
		import wx
		dc = wx.ScreenDC()
	return dc.Size.Get()

def get_window_rect(windowHandle):
	if windowHandle:
		import ctypes
		from locationHelper import RectLTWH
		r = ctypes.wintypes.RECT()
		ctypes.windll.user32.GetWindowRect(windowHandle, ctypes.byref(r))
		return RectLTWH.fromCompatibleType(r)
	return None

def get_current_window_rect():
	import api
	obj = api.getForegroundObject()
	if obj:
		return get_window_rect(obj.windowHandle)
	return None

def take_snapshot_pixels(x=0, y=0, width=None, height=None, current_window=False):
	import screenBitmap
	if current_window:
		rect = get_current_window_rect()
		if not rect:
			return None
		x = rect.left
		y = rect.top
		width = rect.width
		height = rect.height
	else:
		if width is None or height is None: width, height = get_size()
	sb = screenBitmap.ScreenBitmap(width, height)
	return [sb.captureImage(x, y, width, height), x, y, width, height]

def have_curtain():
	import vision
	from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
	screenCurtainId = ScreenCurtainProvider.getSettings().getId()
	screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
	return bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))