from flask import Flask, jsonify, render_template, json, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0',
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/vagrant/marketplace_db.db'
)
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


    def __repr__(self):
        return '<Item %r>' % self.item_name


@app.route('/')
def index():
	return "In progress"


@app.route('/insert/<user_id>/<name>/<description>/<float:price>')
def insert(user_id, name, description, price):
	new_item = Item(user_id, name, description, price)
	db.session.add(new_item)
	db.session.commit()
	return "Item added"


@app.route('/listings')
def listings():
	items = Item.query.all()
	result = ""
	for item in items:
		result += "User ID: " + item.user_id + ", Item Name: " + item.item_name + \
			", Description: " + item.item_description + ", Price: " + str(item.price) \
			+ "\r\n"
	return result
	

if __name__ == '__main__':
	db.create_all()
	app.run(host=app.config['HOST'])