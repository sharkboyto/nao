#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2021-12-16
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import ui
import queueHandler
import speech

def message(msg, queue=False):
	if queue:
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, msg)
	else:
		ui.message(msg)

def queue_message(msg):
	message(msg, queue=True)

def cancel():
	speech.cancelSpeech()

def suppress_typed_characters(count=1):
	speech._suppressSpeakTypedCharacters(count)