import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

from Map import Map

class Account(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	gplusId = ndb.StringProperty()
	accessToken = ndb.StringProperty()
	loggedIn = ndb.BooleanProperty()
	mapIds = ndb.StringProperty(repeated=True)
	adminMaps = ndb.IntegerProperty(repeated=True)

	def to_dict(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'adminMaps':self.adminMaps,
			}

	def get(self):
		return json.dumps(self.to_dict())

	def getMaps(self):
		maps = []
		for mapid in self.adminMaps:
			map = Map.get_by_id(mapid)
			if map is not None:
				maps.append(map.to_dict())
		return json.dumps(maps)

