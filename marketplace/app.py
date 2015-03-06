from flask import Flask, jsonify, render_template, json, request
from db import db_session
from flask.ext.sqlalchemy import SQLAlchemy
from app import models
<<<<<<< HEAD
from flask_oauth import OAuth
=======
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse # Parse through requests
import re # For regular expressions
>>>>>>> adicu/master:marketplace/marketplace.py
GOOGLE_CLIENT_ID = 1077285924024-51aofukoknvs52a6tlsa8oetfdsecsgp.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = dgQpe2OD1_rJDw66cKMv_OXc
REDIRECT_URI = https://www.example.com/oauth2callback

SECRET_KEY = 'development key'

# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"
=======

>>>>>>> parent of f7ece01... Merge remote-tracking branch 'adicu/master'

app = Flask(__name__)

# Import configuration from Flask
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0'
)
db = SQLAlchemy(marketplace)
<<<<<<< HEAD
=======
db = SQLAlchemy(app)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
						   base_url = 
						   authorize_url =
						   request_token_url = None
						   request_token_params)

#https://github.com/mitsuhiko/flask-oauth/blob/master/example/google.py
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

=======
>>>>>>> parent of f7ece01... Merge remote-tracking branch 'adicu/master'

@app.teardown_appcontext
def shutdown_session(exception=None):
	''' Cleanup the database when we close'''
	db_session.remove()


@app.route('/')
def index():
	return "Marketplace"

<<<<<<< HEAD
@app.route('/auth')
def auth():
	
=======

>>>>>>> adicu/master
if __name__ == '__main__':
	app.run(host=app.config['HOST'])