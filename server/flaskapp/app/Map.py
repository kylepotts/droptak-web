import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

class Map(ndb.Model):
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	takIds = ndb.StringProperty(repeated=True)
	name = ndb.StringProperty()
	adminIds = ndb.IntegerProperty(repeated=True)


	def to_dict(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'creator': self.creator,
			'creatorId': self.creatorId,
			}
	
