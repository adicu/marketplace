from flask import Flask, g, jsonify, render_template, json, request
from db import db_session
from flask.ext.sqlalchemy import SQLAlchemy
from oauth2client.client import flow_from_clientsecrets
import httplib2
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse  # Parse through requests
import re

# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"

#Initialize OAuth2.0 values
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    HOST='0.0.0.0',
    SQLALCHEMY_DATABASE_URI='sqlite:////home/vagrant/marketplace_db.db'
)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
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
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'percent': self.percent
        }

# Association table for associating items with tags and vice-versa
item_tags = db.Table('item_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    item_name = db.Column(db.String(200))
    item_description = db.Column(db.String(2000))
    price = db.Column(db.Float)

    # Reference to the tags table
    tags = db.relationship('Tag', secondary=item_tags, backref=db.backref('items', lazy='dynamic'))

    def __init__(self, user_id, item_name, item_description, price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price

    def __repr__(self):
        return '<Item %r>' % self.item_name

    @property
    def serialize(self):
        """ Used for JSONify and render templates """
        tag_output = []
        for tag in self.tags:
            tag_output.append(tag.serialize)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'price': self.price,
            'tags': tag_output
        }

		
@app.route('/')
def index():
    return "In progress"


@app.route('/insert/<user_id>/<name>/<description>/<float:price>')
def insert(user_id, name, description, price):
    new_item = Item(user_id, name, description, price)
    db.session.add(new_item)
    db.session.commit()
    return "Item added with id: " + str(new_item.id)


@app.route('/tag_item/<item_id>/<tag>')
def tag_item(item_id, tag):
    # Get matching item
    matching_items = db.session.query(Item).filter_by(id=item_id).all()
    if len(matching_items) == 0:
        return "No matching items found!"
    if len(matching_items) > 1:
        return "Too many items found!"

    # Get existing item tags and ensure not already there
    item_tags = matching_items[0].tags
    exists = False
    for existing_tag in item_tags:
        if existing_tag.name == tag:
            exists = True
    if exists:
        return "Already exists!"

    # If not, see if the tag is already in the tag database
    tag_t = ""
    matching_tags = db.session.query(Tag).filter_by(name=tag).all()
    if len(matching_tags) == 0:
        # No? Create tag
        tag_t = Tag(tag)
        db.session.add(tag_t)
        db.session.commit()
    else:
        # Add item to new/existing tag
        tag_t = matching_tags[0]

    # Pair up item with tag
    matching_items[0].tags.append(tag_t)
    db.session.commit()

    return "Added tag!"


@app.route('/listings')
def listings():
    items = Item.query.all()
    return jsonify(data=[item.serialize for item in items])
    #return render_template('primary_user_interface.html', data=[item.serialize for item in items])


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
    """
    Post Google sign in, register (and redirect) as necessary or return to listings
    """
    matching_users = User.query.filter_by(user_id=email).all()
    matches = len(matching_users)
    if matches == 0:
        return register(email, name)
    elif matches == 1:
        return jsonify(data=[user.serialize for user in matching_users])
    return "Error!"


def register(email, name):
    """
    Register a new user.
    """
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


@app.route('/auth')
def auth():
	#get authentication code from params
	code = request.args.get('code')
	if not code:
		return render_template('auth.html',
								success = False)
	try:
		#Google+ ID

		#Configure the client object
		oauth_flow = flow_from_clientsecrets(
			'client_secrets.json', 
			scope='',
			redirect_uri = REDIRECT_URI)

		#Redirect to Google's OAuth 2.0 server
		auth_uri = flow.step1_get_authorize_url()

		#Exchange an authorization code for an access token
		credentials = oauth_flow.step2_exchange(code)
		#Apply access token to an Http object
		gplus_id = credentials.id_token['sub']

		#Get first email address from Google+ ID
		http = httplib2.Http()
		http = credentials.authorize(http)

		h, content = http.request('https://www.googleapis.com/plus/v1/people/' 
								   + gplus_id, 'GET')
		data = json.loads(content)
		email = data["emails"][0]["value"]
		name = data['displayName']
		return signin(email, name)

	except Exception as e:
		print e
		return "Error has occurred"
		
		
if __name__ == '__main__':
    db.create_all()
    app.run(host=app.config['HOST'])
