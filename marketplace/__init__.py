# Core application logic
from flask import Flask, jsonify, url_for, session, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from oauth2client.client import OAuth2WebServerFlow
from functools import wraps
import json

app = Flask(__name__)
client_secrets_file = json.loads(open('client_secrets.json', 'r').read())
app.config.update(
    DEBUG=True,
    HOST='0.0.0.0',
    SECRET_KEY='muchsecret',
    GOOGLE_LOGIN_CLIENT_ID=client_secrets_file["web"]["client_id"],
    GOOGLE_LOGIN_CLIENT_SECRET=client_secrets_file["web"]["client_secret"],
    SQLALCHEMY_DATABASE_URI='sqlite:////home/vagrant/marketplace_db.db',
    GOOGLE_LOGIN_REDIRECT_SCHEME="http"
)

# Create the database object, which we use in the models below
db = SQLAlchemy(app)

# Create the login flow
flow = OAuth2WebServerFlow(client_id=app.config['GOOGLE_LOGIN_CLIENT_ID'],
                           client_secret=app.config['GOOGLE_LOGIN_CLIENT_SECRET'],
                           scope='https://www.googleapis.com/auth/userinfo.email',
                           redirect_uri='http://localhost:5000/login/google')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or session["logged_in"] == False:
            return "Authentication required!"
        return f(*args, **kwargs)
    return decorated_function

# Register our routes
from marketplace.routes.home import home
app.register_blueprint(home)

from marketplace.routes.auth import auth
app.register_blueprint(auth)

from marketplace.routes.insert import insert
app.register_blueprint(insert)

from marketplace.routes.listings import listings
app.register_blueprint(listings)

from marketplace.routes.rate_user import rate_user
app.register_blueprint(rate_user)

from marketplace.routes.tag_item import tag_item
app.register_blueprint(tag_item)

from marketplace.routes.update_tags import update_tags
app.register_blueprint(update_tags)

# Ensure the database exists
db.create_all()