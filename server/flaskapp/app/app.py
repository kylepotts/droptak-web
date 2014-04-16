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

from flask import Flask, render_template, request, jsonify, redirect, url_for, g, session,flash
from blueprints.example.views import bp as example_blueprint


app = Flask(__name__)
app.secret_key = 'key'
currentAccount = 1

#the following appends headers to every request to tell the client not to cache contents
#TODO: remove for final demo and submission
@app.after_request
def after_request(response):
	logging.info("attaching no cache header")
	response.headers.add('Cache-Control', 'no-cache, no-store') # http-1.1
	response.headers.add('Pragma', 'no-cache') # http-1
	return response

@app.route('/dash')
def logoutIndex():
		return render_template('dashboard.html')


@app.route('/')
def index():
	if "userId" in session:
		#logging.info("loggedIn=" + str(session['loggedIn']))
		account = Account.get_by_id(session['userId'])
		if account is None: # prevent interal error
			return render_template('index.html')
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
	userMaps = getMaps(session['userId'])
	listOfMaps = []
	for mapId in userMaps:
		logging.info(mapId)
		aMap = Map.get_by_id(mapId)
		listOfMaps.append(aMap.to_dict())
	return json.dumps(listOfMaps)
	return '200'
	#return render_template('map.html', maps=getUserMaps(session['userId']))

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
		session.clear() 
		return '200'

	if request.method == 'GET':
		return render_template('logout.html')

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

@app.route('/app/')
def route_view_app():
	return render_template('view_maps.html');


@app.route('/create/',methods=['GET','POST'])
def create_tak():
	if request.method == 'POST':
		# login required
		mapId = getValue(request, "mapId", "")
		logging.info("mapId="+mapId)
		map = Map.get_by_id(int(mapId))
		if map is None:
			return jsonify(message="Map does not exist", response=400) 
		logging.info("mapid %s" %mapId)
		title = getValue(request, "title", "")
		lat = getValue(request, "lat", "")
		lng = getValue(request, "lng", "")
		#user = getValue(request, "user", "")
		#change form to not supply user
		user = session['username']
		uid = session['userId']
			
		if not ( user and lat and lng ):
			return jsonify(message="Bad Request", response=400)
			# check if args blank

		logging.info("Add lat %s, lng %s" %(lat, lng) )
		tak  = Tak(lng=lng,lat=lat, creator=user, title=title,mapId=mapId,creatorId=uid)
		key = tak.put()
		map.takIds.append(str(key.id()))
		map.put();
		return redirect(url_for('show_taks', id=key.id()))

	if request.method == 'GET': 
		# return list of maps too for selecting
		listOfMaps = []
		mapIds = getMaps(session['userId'])
		for mapid in mapIds:
			ownMap = Map.get_by_id(mapid)
			listOfMaps.append(ownMap)

		return render_template('create_tak.html', maps=listOfMaps)
@app.route('/maps/<mapName>/',methods=['GET','POST'])
@app.route('/maps/<int:mapId>/',methods=['GET','POST'])
def taks(mapId=-1, mapName=''):
	logging.info("in taks")
	if mapName != '':
		qry = getUserMaps(session['userId'])
		qry = qry.filter(Map.name == mapName)
		mapId = qry.get().key.integer_id()
		logging.info("MapID %s" %mapId)

	if mapId == "":
		return redirect('/app')
	map = Map.get_by_id(mapId)
	if map is None:
		return redirect('/app')
	taks = getMapTaks(str(mapId))
	return render_template('view_taks.html',taks = taks, mapName=map.name)

@app.route('/taks/<int:id>', methods = ['GET', 'POST'])
def show_taks(id=-1):
	if request.method == 'GET':
		if id >= 0:
			tak = Tak.get_by_id(id)
			if tak is not None:
				return tak.view()
	return redirect('/app')

@app.route('/maps/new', methods=['GET','POST'])
def create_map():
	if request.method == 'GET':
		return '200'
	if request.method == 'POST':
		user =  session['username']
		userId = session['userId']
		mapName = getValue(request, "name", "")
		admin = [userId]
		ownMap = Map(creator=user,creatorId=userId,name=mapName,adminIds=admin)
		key = ownMap.put()

		adminAccount = Account.get_by_id(userId)
		adminAccount.adminMaps.append(key.integer_id())
		adminAccount.put()
		return json.dumps(ownMap.to_dict())

@app.route('/map/admin/<int:mapId>/<string:email>',methods=['GET','POST'])
def admin_add(mapId,email):
	if request.method == 'POST':
		logging.info("email="+email)
		user = session['username']
		uid = session['userId']
		map = Map.get_by_id(mapId)
		adminAccount = Account.query(Account.email == email).get()
		adminId = adminAccount.key.integer_id()
		if adminId not in map.adminIds:
			map.adminIds.append(adminId)
			map.put()
		if mapId not in adminAccount.adminMaps:
			adminAccount.adminMaps.append(mapId)
			adminAccount.put()

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

def getMaps(id):
	account = Account.get_by_id(id)
	return account.adminMaps

def getMapTaks(id):
	query = Tak.query(Tak.mapId == id)
	return query

# returns taks in map
@app.route('/api/maps/<int:id>/', methods=['GET','POST', 'DELETE', 'PUT'])
def api_taks(id=-1):
	if request.method == 'GET':
		query = getMapTaks(str(id));
		if query.count == 0:
			return json.dumps({})
		else:
			return json.dumps([t.to_dict() for t in query.fetch()])
	if request.method == 'DELETE':
		map = Map.get_by_id(id)
		logging.info("DELETE " + str(id))
		if map is not None:
			# remove taks in map
			for takid in map.takIds:
				tak = Tak.get_by_id(int(takid))
				logging.info("_DELETE sub-tak" + str(takid))
				if tak is not None:
					tak.key.delete()
			for mid in map.adminIds:
				logging.info("mid="+str(mid))
				adminAcct = Account.get_by_id(mid)
				adminAcct.adminMaps.remove(id)
				adminAcct.put()
			map.key.delete()
			return "Success"
		return "Map does not exist"


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
	    	account = query.get()
	    	if query.count() != 0:
	    		logging.info("Account Already Exists")
	    		key = account.key
	    		return json.dumps({"uuid":key.integer_id()
    			})

	    	logging.info("first time logging in")
	    	session['gplus_id'] = gplus_id
	    	session['username'] = name 
	    	account = Account(name=name,email=email,gplusId=gplus_id,accessToken=access_token,loggedIn=True)
	    	key = account.put()
	    	session['userId'] = key.integer_id()
    		return json.dumps({"uuid":key.integer_id()
    			})

		if request.method == 'GET':
			return page_not_found(404)
@app.route('/api/map',methods=['GET','POST'])
def api_map():
	if request.method == 'POST':
		userName = request.args.get("username","")
		mapName = request.args.get("mapname","")
		userId = request.args.get("userId","")
		userId = str(userId.encode('utf-8').decode('ascii', 'ignore'))
		uid = int(userId)
		ownMap =Map(creator=userName,creatorId=uid,name=mapName)
		key = ownMap.put()
		return json.dumps({"mapId":key.integer_id()}) 

	if request.method == 'GET':
		id = request.args.get("id","")
		ownMap = Map.get_by_id(int(id))
		return json.dumps({"creator":ownMap.creator,"name":ownMap.name,"creatorId":ownMap.creatorId,"id":int(id)})

@app.route('/api/tak',methods=['GET','POST'])
def api_tak():
	if request.method == 'POST':
		userName = request.args.get("name","")
		mapId = request.args.get("mapId","")
		mapId = str(mapId.encode('utf-8').decode('ascii', 'ignore'))
		userId = request.args.get("id","")
		userId = int(str(userId.encode('utf-8').decode('ascii', 'ignore')))
		title = request.args.get("title","")
		lat = request.args.get("lat","")
		lat = str(lat.encode('utf-8').decode('ascii', 'ignore'))
		lng = request.args.get("lng","")
		lng =str(lng.encode('utf-8').decode('ascii', 'ignore'))
		tak = Tak(title=title,lat=lat,lng=lng,creator=userName,creatorId=userId,mapId=mapId)
		key = tak.put()
		logging.info("tak added")
		return json.dumps({"takId":key.integer_id()})
	if request.method == 'GET':
		return '200'

@app.route('/api/tak/<int:id>',methods=['GET','POST','PUT', 'DELETE'])
def api_single_tak(id=-1):
	tak = Tak.get_by_id(id)
	if tak is None:
		return '404: '

	if request.method == 'GET':
		return json.dumps(tak.to_dict())

	if request.method == 'DELETE':
		# TODO: first find what map it's in and delete it from there
		tak.key.delete()
		return '200'

	if request.method == 'PUT':
		title = getValue(request, "title", "")
		logging.info("title: " + title)
		tak.update(title=title)
		tak.put()
		return '200'

	if request.method == 'POST':
		return '200'

#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# 						START OFFICIAL API ROUTING
#
# 
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#/api/v1/search?<key1>=<value1>&<key2>=<value2>
#/api/v1/search?name=<name>
#	GET only
#	No authentication -> public maps only
#	Authentication -> public maps + personal maps + maps shared with that person
#	
#	example keys:
#id: maps only from this user id
#name: maps with name equal to this value
#taks: true or false, include searching of tak data, false by default  
#<key>=<value>: unmapped keys look for maps with that key and value in meta-data

#/api/v1/user/<user id>/
@app.route('/api/v1/user/<int:userid>/',methods=['GET'])
def userData(userid = -1):
	if request.method == 'GET':
#	GET: returns json object of user
		return '200'
#	these require higher security:
#	POST none
#	PUT: update user info
#	DELETE: delete user


#/api/v1/user/<user id>/maps/
@app.route('/api/v1/user/<int:userid>/maps/',methods=['GET','POST'])
def mapsForUser(userid = -1):
	if request.method == 'GET':
#		GET: returns json array of users map objects
		return '200'
	if request.method == 'POST':
# parameters: name
# returns json map object created
#		POST: used to create maps
		return '200'

#/api/v1/maps/<map id>/taks/	
@app.route('/api/v1/maps/<int:mapid>/taks/',methods=['GET','POST'])
def taksForMap(mapid = -1):
	if request.method == 'GET':
#		GET: json data of taks in selected map
		return '200'
	if request.method == 'POST':
# POST: Creates a tak for user, return tak object
		return '200'


#/api/v1/maps/<map id>/
@app.route('/api/v1/maps/<int:mapid>/',methods=['GET','POST','PUT', 'DELETE'])
def mapData(mapid = -1):
	if request.method == 'GET':
		# parameters: none
		# returns json object of map + inner array of tak ids

		return '200'

	if request.method == 'DELETE':
		# DELETE: used to delete a map object and all associated tak objects, parameters: none
		return '200'

	if request.method == 'PUT':
		#PUT: 	used to update map in database, parameters: (any map parameter)
		# return json map object
		return '200'

	if request.method == 'POST':
		# no action
		return '200'
	


#/api/v1/taks/<tak id>
@app.route('/api/v1/taks/<int:takid>/',methods=['GET','POST','PUT', 'DELETE'])
def takData(mapid = -1):
	if request.method == 'GET':
		# GET: returns a single json tak object
		return '200'

	if request.method == 'DELETE':
		# DELETE: deletes that tak
		return '200'

	if request.method == 'PUT':
		# PUT: updates a tak returns that object
		return '200'

	if request.method == 'POST':
		# no action
		return '200'

#updating map/tak attributes
#/api/v1/<maps | taks>/<mapid | takid>/ <attribute-name>
#	common attributes:
#		title, name, lat, lng, privacy
#	else: add to list of attributes
#	POST: new attribute
#	PUT: edit existing attribute, params: value
#	GET: get attribute
#	DELETE: delete only from list of attributes
#
#/api/v1/maps/<map id>/admins/<email | userid?>
#	POST:  Add a admin to current list of admins for a map with id mapid
#	GET: returns array of userIds of the admins assigned to the map
#	DELETE: Remove admin from the list of current admins for the  map
	

#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# 						END OFFICIAL API ROUTING
#
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# register Blueprints
app.register_blueprint(example_blueprint)

