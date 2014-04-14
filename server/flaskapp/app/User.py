import json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

class Account(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	gplusId = ndb.StringProperty()
	accessToken = ndb.StringProperty()
	loggedIn = ndb.BooleanProperty()
	mapIds = ndb.StringProperty(repeated=True)