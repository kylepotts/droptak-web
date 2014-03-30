from utils.path import fix_path
import os, json
from google.appengine.api.logservice import logservice
import logging
import random
import string
import httplib2
import uuid
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
	if "userId" in session:
		logging.info("loggedIn=" + str(session['loggedIn']))
		account = Account.get_by_id(session['userId'])
		lin = account.loggedIn
		logging.info("lin="+str(lin))
		if lin == False:
			return render_template('index.html')
		if lin == True:
			return render_template('dashboard.html')

	if session:
		return render_template('dashboard.html')
	else:
		return render_template('index.html')

@app.route('/maps/',methods=['GET','POST'])
def maps():
	return render_template('map.html', maps=getUserMaps(session['userId']))

@app.route('/logout',methods=['GET','POST'])
def logout():
	if request.method == 'POST':
		name = session['username']
		account = Account.query(Account.name == name).get()
		account.loggedIn = False
		account.put()
		logging.info("session before " + str(len(session)))
		logging.info("session after " + str(len(session)))
		session['loggedIn'] = False
		logging.info("session set to loggedin = false")
		#return redirect(url_for('index'),code=302)
		return '200'
@app.route('/login',methods=['GET','POST'])
def login():
		if request.method == 'POST':
			name = request.args.get("name","")
			email =  request.args.get("email","")
			logging.info("name " + name +" email " + email)
			account = Account.query(Account.email == email).get()
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
    			return page_not_found(404)

	    	# once store token verified send a request for credential for gplus
	    	access_token = credentials.access_token
	    	logging.info(access_token)
	    	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"% access_token)
	    	h = httplib2.Http()
	    	result = json.loads(h.request(url,'GET')[1])
	    	gplus_id = credentials.id_token['sub']
	    	stored_credentials = session.get('credentials')
	    	stored_gplus_id = session.get('gplus_id')

	    	if account is not None:
	    		logging.info("User already logged in")
	    		account = Account.query(Account.email == email).get()
	    		account.loggedIn = True
	    		account.put()
	    		session['credentials'] = credentials
	    		session['gplus_id'] = gplus_id
	    		session['username'] = account.name
	    		session['userId'] = account.key.integer_id()
	    		session['loggedIn'] = True


	    	else:
	    		logging.info("first time logging in")
	    		session['credentials'] = credentials
	    		session['gplus_id'] = gplus_id
	    		session['username'] = name 
	    		account = Account(name=name,email=email,gplusId=gplus_id,accessToken = access_token,loggedIn=True)
	    		key = account.put()
	    		session['userId'] = key.integer_id()
	    		session['loggedIn'] = True

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
		return render_template('create_tak.html', maps=getUserMaps(session['userId']))
@app.route('/maps/<mapName>/',methods=['GET','POST'])
@app.route('/maps/<int:mapId>/',methods=['GET','POST'])
def taks(mapId=-1, mapName=''):
	logging.info("in taks")
	if mapName != '':
		logging.info("empty map name")
		qry = getUserMaps(session['userId'])
		qry = qry.filter(Map.name == mapName)
		mapId = qry.get().key.integer_id()
		logging.info("MapID %s" %mapId)

	if mapId == "":
		return
	taks = getMapTaks(str(mapId))
	return render_template('view_taks.html',taks = taks)

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
	logging.info("getUserMaps id is " + str(id))
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

@app.route('/api/login',methods=['GET','POST'])
def api_login():
		logging.info("api_login Type "+ request.method)
		if request.method == 'POST':
			name = request.args.get("name","")
			email =  request.args.get("email","")
			logging.info("name " + name +" email " + email)


    		# once store token verified send a request for credential for gplus
	    	access_token = request.args.get("storeToken","")
	    	gplus_id = request.args.get("id","")
	    	logging.info(access_token)
	    	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"% access_token)
	    	h = httplib2.Http()
	    	result = json.loads(h.request(url,'GET')[1])
	    	query = Account.query(Account.email == email)
	    	if query.count() != 0:
	    		logging.info("Account Already Exists")
	    		return '200'

	    	logging.info("first time logging in")
	    	session['gplus_id'] = gplus_id
	    	session['username'] = name 
	    	account = Account(name=name,email=email,gplusId=gplus_id,accessToken=access_token,loggedIn=True)
	    	key = account.put()
	    	session['userId'] = key.integer_id()
	    	uid = uuid.uuid4()
    		return json.dumps({"uuid":uid.hex
    			})

		if request.method == 'GET':
			return page_not_found(404)


# register Blueprints
app.register_blueprint(example_blueprint)

