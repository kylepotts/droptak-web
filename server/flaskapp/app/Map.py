import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

class Map(ndb.Model):
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	takIds = ndb.StringProperty(repeated=True)
	name = ndb.StringProperty()
	public = ndb.BooleanProperty()
	tags = ndb.JsonProperty()


	def to_dict(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'creator': self.creator,
			'creatorId': self.creatorId,
			'public': self.public,
			'tags' : self.tags,
			}

	# api class controller for GET method
	def Get(self):
		
		return

	# api class controller for PUT method
	def Put(self):

		return

	# api class controller for DELETE method
	def Delete(self):
		return

	# api class controller for POST method
	def Post(self):
		return
	
