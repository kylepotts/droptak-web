from utils.path import fix_path
import os, json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
import Map

class Tak(ndb.Model):
	name = ndb.StringProperty() # latitude
	lat = ndb.StringProperty() # latitude
	lng = ndb.StringProperty() # longitude
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	mapId = ndb.IntegerProperty()
	metadata = ndb.JsonProperty()

	def to_dict(self):
		return {
			'name' : self.name,
			'id': self.key.id(),
			'lat': self.lat,
			'lng': self.lng,
			'creator': {
				'name': self.creator,
				'id': self.creatorId,
			},
			'mapid': self.mapId,
			'metadata' : self.metadata,
			}

	# api class controller for GET method
	def Get(self):
		return self.to_dict()

	# api class controller for PUT method
	def Put(self):

		return

	# api class controller for DELETE method
	def Delete(self):
		map = Map.Map.get_by_id(self.mapId)
		if map is not None:
			map.takIds.remove(self.key.integer_id())
			map.put()
		self.key.delete()
		return

	# api class controller for POST method
	def Post(self):
		return

	def update(self, name):
		self.name = name
		return

	def view(self):
		return render_template('edit_tak.html',id=self.key.id())

