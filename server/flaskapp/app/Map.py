import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

from Tak import Tak 

class Map(ndb.Model):
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	takIds = ndb.StringProperty(repeated=True)
	name = ndb.StringProperty()
	
	public = ndb.BooleanProperty()
	data = ndb.JsonProperty()

	adminIds = ndb.IntegerProperty(repeated=True)


	def to_dict(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'creator': self.creator,
			'creatorId': self.creatorId,
			'takIds': self.takIds,
			'public': self.public,
			'data' : self.data,
			'adminIds':self.adminIds,
			}

	# api class controller for GET method
	def get(self):
		return json.dumps(self.to_dict())

	def getTaks(self):
		taks = []
		for takid in self.takIds:
			tak = Tak.get_by_id(int(takid))
			if tak is not None:
				taks.append(tak.to_dict())
		return json.dumps(taks)

	# api class controller for PUT method
	def put(self):

		return

	# api class controller for DELETE method
	def delete(self):
		return

	# api class controller for POST method
	def post(self):
		return
	
