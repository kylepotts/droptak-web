import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

class Tak(ndb.Model):
	title = ndb.StringProperty() # latitude
	lat = ndb.StringProperty() # latitude
	lng = ndb.StringProperty() # longitude
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()

	def to_dict(self):
		return {
			'id': self.key.id(),
			'lat': self.lat,
			'lng': self.lng,
			'creator': self.creator,
			'creatorId': self.creatorId,
			}


