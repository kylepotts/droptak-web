import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

class Map(ndb.Model):
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	takIds = ndb.StringProperty(repeated=True)
	name = ndb.StringProperty()
	
