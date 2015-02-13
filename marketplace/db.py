from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(200), unique=True)
	name = db.Column(db.String(100), unique=True)
	percent = db.Column(db.Integer)

	def __init__(self, user_id, email, name, percent):
		self.user_id = user_id
		self.email = email
		self.name = name
		self.percent = percent

	def __repr__(self):
		return '<User %r>' % self.user_id