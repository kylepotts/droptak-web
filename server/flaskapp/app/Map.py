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


	def to_dict(self):
		owner = User.Account.get_by_id(int(self.creatorId))
		ownerdata = {}
		if owner is not None:
			ownerdata = owner.to_dict()
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
			'owner': ownerdata,
			'taks': taks,
			'public': str(self.public),
			'admins': admins,
			}

	def getInfo(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'public': str(self.public),
			}

	# api class controller for GET method
	def Get(self):
		return self.to_dict()

	# api class controller for PUT method
	def Put(self, newName="", newIsPublic="",newOwner=""):
		if newName != "":
			self.name = newName

		if newIsPublic != "":
			isPublic = False
			if newIsPublic == "true":
				isPublic = True
			elif newIsPublic == "false":
				isPublic = False
			logging.info("isPublic="+str(isPublic))
			self.public = isPublic

		if newOwner != "":
			newId = int(newOwner)
			newOwnerAccount = User.Account.get_by_id(newId)
			self.creator = newOwnerAccount.name
			self.creatorId = newOwnerAccount.key().integer_id()
		self.put()
		return

	# api class controller for DELETE method
	def Delete(self):
		# remove taks in map
		for takid in self.takIds:
			tak = Tak.get_by_id(int(takid))
			if tak is not None:
				tak.key.delete()
		for mid in self.adminIds:
			admin = User.Account.get_by_id(mid)
			if admin is not None:
				admin.adminMaps.remove(self.key.integer_id())
				admin.put()
		self.key.delete()
		return

	# api class controller for POST method
	def Post(self):
		return
	
