from utils.path import fix_path
import os, json
from google.appengine.api.logservice import logservice
import logging
from User import Account 
from Tak import Tak 
from Map import Map

# this fix allows us to import modues/packages found in 'lib'
fix_path(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session
from blueprints.example.views import bp as example_blueprint


app = Flask(__name__)
app.secret_key = 'key'
currentAccount = 1
app.debug = True


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/maps/',methods=['GET','POST'])
def maps():
	return render_template('map.html', maps=getUserMaps(session['userId']))

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
				key = account.put()
				logging.info(type(key))
				session['userId'] = key.integer_id()

			else:
				foundAccount = query.get()
				session['userId'] = foundAccount.key.integer_id()
				logging.info("account already exists")
			logging.info("Logged in")

			session['username'] = name
			return '200'
	if request.method == 'GET':
		return page_not_found(404)


@app.route('/create/',methods=['GET','POST'])
def create_tak():
	if request.method == 'POST':
			# login required
			mapId = getValue(request, "mapId", "")
			logging.info("mapid %s" %mapId)
			title = getValue(request, "title", "")
			lat = getValue(request, "lat", "")
			lng = getValue(request, "lng", "")
			#user = getValue(request, "user", "")
			#change form to not supply user
			user = session['username']
			
			if not ( user and lat and lng ):
				return jsonify(message="Bad Request", response=400)
			# check if args blank
			logging.info("Add lat %s, lng %s" %(lat, lng) )
			tak  = Tak(lng=lng,lat=lat, creator=user, title=title,mapId=mapId)
			key = tak.put()
			return redirect(url_for('show_taks', id=key.id()))
	if request.method == 'GET': 
		# return list of maps too for selecting
		return render_template('taks.html', maps=getUserMaps(session['userId']))
@app.route('/maps/<mapName>/',methods=['GET','POST'])
@app.route('/maps/<int:mapId>/',methods=['GET','POST'])
def taks(mapId=-1, mapName=''):
	if mapName != '':
		qry = getUserMaps(session['userId'])
		qry = qry.filter(Map.name == mapName)
		mapId = qry.get().key.integer_id()
		logging.info("MapID %s" %mapId)

	if mapId == "":
		return
	taks = getMapTaks(str(mapId))
	return render_template('all_taks.html',taks = taks)

@app.route('/taks/<int:id>', methods = ['GET', 'POST'])
def show_taks(id=-1):
	if request.method == 'GET':
		if id >= 0:
			tak = Tak.get_by_id(id)
			if tak is not None:
				return tak.view()
	return redirect('/maps')

@app.route('/maps/new', methods=['GET','POST'])
def create_map():
	if request.method == 'GET':
		return '200'
	if request.method == 'POST':
		user =  session['username']
		userId = session['userId']
		mapName = request.args.get("name","")
		ownMap = Map(creator=user,creatorId=userId,name=mapName)
		ownMap.put()
		return '200'

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
				print "Item requested not accessible"
				value = default
	return value

def getUserMaps(id):
	query = Map.query(Map.creatorId == id)
	return query
def getMapTaks(id):
	query = Tak.query(Tak.mapId == id)
	return query



@app.route('/api/taks/')
def api_taks():
	user = getValue(request, "user", "")
	if user:
		query = Tak.query(Tak.creator == user)
	else: query = Tak.query()
	return json.dumps([t.to_dict() for t in query.fetch()])

# register Blueprints
app.register_blueprint(example_blueprint)

