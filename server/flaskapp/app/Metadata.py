from utils.path import fix_path
import os, json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

class Metadata(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

	def to_dict(self):
		return {
			"key":self.key,
			"value":self.value
		}
