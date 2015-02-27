from flask import Flask, jsonify, render_template, json, request
from db import db_session
from flask.ext.sqlalchemy import SQLAlchemy
from app import models


app = Flask(__name__)

# Import configuration from Flask
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0'
)
db = SQLAlchemy(marketplace)

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