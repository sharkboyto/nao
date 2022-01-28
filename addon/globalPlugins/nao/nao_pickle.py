#Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Last update 2022-01-28
#Copyright (C) 2021 Alessandro Albano, Davide De Carne and Simone Dal Maso

import os
import globalVars
from .framework.storage.pickle import Pickle as PickleLib

class NaoPickle:
	class Pickle(PickleLib):
		def __singleton_init__(self, path, name):
			super(NaoPickle.Pickle, self).__singleton_init__(path, name)
			if not self.file_exists:
				#check for the old version
				prev = os.path.join(globalVars.appArgs.configPath, "nao.pickle")
				try:
					if os.path.isfile(prev):
						self._makedirs()
						import shutil
						shutil.move(prev, self.file_name)
				except:
					pass
				if not self.file_exists:
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

	def __new__(cls):
		return NaoPickle.Pickle(os.path.join(globalVars.appArgs.configPath, "nao"), "nao.pickle")