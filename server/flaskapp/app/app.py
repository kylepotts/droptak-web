from utils.path import fix_path
import os
from google.appengine.api.logservice import logservice
import logging
from User import Account 
from Tak import Tak 

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from blueprints.example.views import bp as example_blueprint


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maps')
def maps():
    return render_template('map.html')
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
			name = request.args.get("name", "")
			email = request.args.get("email", "")
			# check if arg blank
			logging.info("Name %s" %name)
			logging.info("Email %s" %email)
			account  = Account(name=name,email=email)
			query = Account.query(Account.email == email)
			logging.info(query.count())
			if query.count() == 0:
				account.put()
			return '200'
	if request.method == 'GET':
		return page_not_found(404)


@app.route('/taks/',methods=['GET','POST'])
def taks():
	if request.method == 'POST':
			title = getValue(request, "title", "")
			lat = getValue(request, "lat", "")
			lng = getValue(request, "lng", "")
			user = getValue(request, "user", "")
			if not ( user and lat and lng ):
				return jsonify(message="Bad Request", response=400)
			# check if args blank
			logging.info("Add lat %s, lng %s" %(lat, lng) )
			tak  = Tak(lng=lng,lat=lat, creator=user, title=title)
			key = tak.put()
			return redirect(url_for('show_taks', id=key.id()))
	if request.method == 'GET':
		return render_template('taks.html')

@app.route('/taks/<int:id>', methods = ['GET', 'POST'])
def show_taks(id=-1):
	if request.method == 'GET':
		if id >= 0:
			tak = Tak.get_by_id(id)
			if tak is not None:
				return jsonify(tak.to_dict())
	return redirect('/taks')

@app.errorhandler(404)
def page_not_found(e):
    return '404: Page Not Found'

def getValue(request, key, default):
	value = default
	if request is not None:
		value = request.args.get(key, default)
		if value is default:
			try:
				value = request.form[key]
			except KeyError:
				print "Key Error"
				value = default
	return value

# register Blueprints
app.register_blueprint(example_blueprint)
