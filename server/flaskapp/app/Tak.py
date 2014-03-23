from utils.path import fix_path
import os, json
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
import logging

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session

class Tak(ndb.Model):
	title = ndb.StringProperty() # latitude
	lat = ndb.StringProperty() # latitude
	lng = ndb.StringProperty() # longitude
	creator = ndb.StringProperty()
	creatorId = ndb.IntegerProperty()
	mapId = ndb.StringProperty()

	def to_dict(self):
		return {
			'id': self.key.id(),
			'lat': self.lat,
			'lng': self.lng,
			'creator': self.creator,
			'creatorId': self.creatorId,
			}

	def update(self):
		
		return

	def view(self):
		return render_template('edit_tak.html',tak=self)

