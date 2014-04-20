import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging
import User # cyclical import 
from Tak import Tak 

class Map(ndb.Model):
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	takIds = ndb.IntegerProperty(repeated=True)
	name = ndb.StringProperty()
	public = ndb.BooleanProperty()
	adminIds = ndb.IntegerProperty(repeated=True)
	metadata = ndb.JsonProperty()


	def to_dict(self):
		taks = []
		for takid in self.takIds:
			tak = Tak.get_by_id(int(takid))
			if tak is not None:
				taks.append(tak.to_dict())
		admins = []
		for adminid in self.adminIds:
			user = User.Account.get_by_id(int(adminid))
			if user is not None:
				admins.append(user.to_dict())
		return {
			'name' : self.name,
			'id': self.key.id(),
			'owner': {
				'name': self.creator,
				'id': self.creatorId,
			},
			'taks': taks,
			'public': self.public,
			'admins': admins,
			'metadata' : self.metadata,
			}

	# api class controller for GET method
	def Get(self):
		return json.dumps(self.to_dict())

	# api class controller for PUT method
	def Put(self):

		return

	# api class controller for DELETE method
	def Delete(self):
		return

	# api class controller for POST method
	def Post(self):
		return
	
