from flask import Flask, g, jsonify, render_template, json, request
<<<<<<< HEAD:marketplace/app.py
from db import db_session
from flask.ext.sqlalchemy import SQLAlchemy
from app import models
from oauth2client.client import flow_from_clientsecrets
import httplib2
=======
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse # Parse through requests
import re # For regular expressions
>>>>>>> adicu/master:marketplace/marketplace.py

# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"

#Initialize OAuth2.0 values
GOOGLE_CLIENT_ID = '51aofukoknvs52a6tlsa8oetfdsecsgp.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'dgQpe2OD1_rJDw66cKMv_OXc'
REDIRECT_URI = 'https://www.example.com/oauth2callback'
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0',
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/vagrant/marketplace_db.db'
)
<<<<<<< HEAD:marketplace/app.py
db = SQLAlchemy(marketplace)
=======
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    percent = db.Column(db.Integer)


    def __init__(self, user_id, name, percent):
        self.user_id = user_id
        self.name = name
        self.percent = percent


    def __repr__(self):
        return '<User %r>' % self.user_id

    @property
    def serialize(self):
    	""" Used for JSONify and render templates """
    	return {
	    	'id' : self.id,
	    	'user_id' : self.user_id,
	    	'name' : self.name,
	    	'percent' : self.percent
    	}


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    item_name = db.Column(db.String(200))
    item_description = db.Column(db.String(2000))
    price = db.Column(db.Float)


    def __init__(self, user_id, item_name, item_description, price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price

>>>>>>> adicu/master:marketplace/marketplace.py

    def __repr__(self):
        return '<Item %r>' % self.item_name

    @property
    def serialize(self):
    	""" Used for JSONify and render templates """
    	return {
	    	'id' : self.id,
	    	'user_id' : self.user_id,
	    	'item_name' : self.item_name,
	    	'item_description' : self.item_description,
	    	'price' : self.price
    	}



@app.route('/insert/<user_id>/<name>/<description>/<float:price>')
def insert(user_id, name, description, price):
	new_item = Item(user_id, name, description, price)
	db.session.add(new_item)
	db.session.commit()
	return "Item added"


@app.route('/listings')
def listings():
	items = Item.query.all()
	return render_template('results.html', data=[item.serialize for item in items])


@app.route('/fakesignin')
def fakesignin():
	# Get params from the request
	parser = reqparse.RequestParser()
	parser.add_argument('Email', type=str, required=True, help='E-mail must be provided.',
		location='headers')
	parser.add_argument('Name', type=str, required=True, help='Name must be provided.',
		location='headers')
	args = parser.parse_args()
	return signin(args['Email'], args['Name'])


def signin(email, name):
	'''
	Post Google signin, register (and redirect) as necessary or return to listings
	'''
	matching_users = User.query.filter_by(user_id=email).all()
	matches = len(matching_users)
	if matches == 0:
		return register(email, name)
	elif matches == 1:
		return jsonify(data=[user.serialize for user in matching_users])
	return "eww"


def register(email, name):
	'''
	Register a new user.
	'''
	try: 
		# Catch regex
		regex_result = re.match(CU_EMAIL_REGEX, email)
		if not regex_result:
			raise NameError("Invalid e-mail")

		user = User(email, name, 50.0)
		db.session.add(user)
		db.session.commit()
		return "Welcome to Marketplace!"
	except Exception:
		return "We couldn't register you. Make sure you use a Columbia or Barnard email."

<<<<<<< HEAD
@app.route('/auth')
def auth():
	#get code from params
	code = request.args.get('code')
	if not code:
		return render_template('auth.html',
								success = False)
	try:
		#Google+ ID
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
		gplus_id = credentials.id_token['sub']

		#Get first email address from Google+ ID
		http = httplib2.Http()
		http = credentials.authorize(http)

		h, content = http.request('https://www.googleapis.com/plus/v1/people/' 
								   + gplus_id, 'GET')
		data = json.loads(content)
		email = data["emails"][0]["value"]
		name = data['displayName']
		register(email, name)

	except Exception as e:
		print e
		return "Error has occured"
=======

>>>>>>> adicu/master
if __name__ == '__main__':
	db.create_all()
	app.run(host=app.config['HOST'])