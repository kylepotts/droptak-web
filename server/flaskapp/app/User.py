import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging
import Map

class Account(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	gplusId = ndb.StringProperty()
	accessToken = ndb.StringProperty()
	loggedIn = ndb.BooleanProperty()
	mapIds = ndb.IntegerProperty(repeated=True)
	adminMaps = ndb.IntegerProperty(repeated=True)

	def to_dict(self):
		return {
			'name' : self.name,
			'email' : self.email,
			'id': self.key.id(),
			}

	def Get(self):
		return self.to_dict()

	def getMaps(self):
		maps = []
		for mapid in self.adminMaps:
			map = Map.Map.get_by_id(mapid)
			if map is not None:
				maps.append(map.to_dict())
		return maps


