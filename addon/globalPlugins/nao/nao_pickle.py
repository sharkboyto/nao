#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-27
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

from .framework.storage.pickle import Pickle

class NaoPickle(Pickle):
	def __new__(cls):
		return super(NaoPickle, cls).__new__(cls, "nao")

	def __init__(self):
		super(NaoPickle, self).__init__("nao")
		if not self.pickle_file_exists:
			self.start_write()
			self.commit_write()

	@property
	def default_data(self):
		from .framework.generic.updates import PICKLE_UPDATES_DEFAULT_ROOT_NAME, pickle_updates_default_data
		ret = {
			"cache": {
				"documents": {
					"last_purge": 0
				}
			}
		}
		ret[PICKLE_UPDATES_DEFAULT_ROOT_NAME] = pickle_updates_default_data()
		return ret