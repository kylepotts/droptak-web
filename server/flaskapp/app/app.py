from utils.path import fix_path
import os, json
from google.appengine.api.logservice import logservice
import logging
import random
import string
import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
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


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/maps',methods=['GET','POST'])
def maps():
	return render_template('map.html', maps=getUserMaps(session['userId']))

@app.route('/login',methods=['GET','POST'])
def login():

	if request.method == 'POST':
			name = request.args.get("name","")
			email =  request.args.get("email","")
			logging.info("name " + name +" email " + email)
			#create a state string
			state = ''
			for x in xrange(32):
				state+= random.choice(string.ascii_uppercase + string.digits)
    	session['state'] = state
    	storeToken = request.args.get("storeToken","")

    	#verify store token with google servers

    	try:
    		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    		oauth_flow.redirect_uri = 'postmessage'
    		credentials = oauth_flow.step2_exchange(storeToken)
    	except FlowExchangeError:
    		logging.info("error with Oauth")

    	# once store token verified send a request for credential for gplus
    	access_token = credentials.access_token
    	logging.info(access_token)
    	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"% access_token)
    	h = httplib2.Http()
    	result = json.loads(h.request(url,'GET')[1])
    	gplus_id = credentials.id_token['sub']
    	stored_credentials = session.get('credentials')
    	stored_gplus_id = session.get('gplus_id')

    	if stored_credentials is not None and gplus_id == stored_gplus_id:
    		logging.info("User already logged in")
    		account = Account.query(Account.email == email).get()
    		session['credentials'] = credentials
    		session['gplus_id'] = gplus_id
    		session['username'] = account.name
    		session['userId'] = account.key.integer_id()


    	else:
    		logging.info("first time logging in")
    		session['credentials'] = credentials
    		session['gplus_id'] = gplus_id
    		session['username'] = name 
    		account = Account(name=name,email=email,gplusId=gplus_id)
    		key = account.put()
    		session['userId'] = key.integer_id()

    	return '200'

	if request.method == 'GET':
		return page_not_found(404)


@app.route('/taks/new/',methods=['GET','POST'])
def create_tak():
	if request.method == 'POST':
			logging.info("currentMap is "+session['currentMapId'])
			title = getValue(request, "title", "")
			lat = getValue(request, "lat", "")
			lng = getValue(request, "lng", "")
			#user = getValue(request, "user", "")
			user = session['username']
			mapId = session['currentMapId']
			if not ( user and lat and lng ):
				return jsonify(message="Bad Request", response=400)
			# check if args blank
			logging.info("Add lat %s, lng %s" %(lat, lng) )
			tak  = Tak(lng=lng,lat=lat, creator=user, title=title,mapId=mapId)
			key = tak.put()
			return redirect(url_for('show_taks', id=key.id()))
	if request.method == 'GET':
		return render_template('taks.html')
@app.route('/taks/',methods=['GET','POST'])
def taks():
	mapId = request.args.get("mapId","")
	if mapId == "":
		return

	session['currentMapId'] = mapId
	taks = getMapTaks(str(mapId))
	return render_template('all_taks.html',taks = taks)

@app.route('/taks/<int:id>', methods = ['GET', 'POST'])
def show_taks(id=-1):
	if request.method == 'GET':
		if id >= 0:
			tak = Tak.get_by_id(id)
			if tak is not None:
				return render_template('edit_tak.html',tak=tak)
	return redirect('/taks')

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
				print "Key Error"
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


app.debug = True
