from flask import Blueprint, jsonify, render_template, json, request
from marketplace import db
from marketplace.models import User
from oauth2client.client import flow_from_clientsecrets
from datetime import date, datetime
from flask.ext.restful import reqparse  # Parse through requests
import httplib2
import re

auth = Blueprint('auth', __name__)


# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"


@auth.route('/auth')
def authenticate():
    # get authentication code from params
    code = request.args.get('code')
    if not code:
        return render_template('auth.html',
                               success=False)
    try:
        # Google+ ID
        # Configure the client object
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json',
            scope='',
            redirect_uri=REDIRECT_URI)

        # Redirect to Google's OAuth 2.0 server
        auth_uri = flow.step1_get_authorize_url()

        # Exchange an authorization code for an access token
        credentials = oauth_flow.step2_exchange(code)
        # Apply access token to an Http object
        gplus_id = credentials.id_token['sub']

        # Get first email address from Google+ ID
        http = httplib2.Http()
        http = credentials.authorize(http)

        h, content = http.request('https://www.googleapis.com/plus/v1/people/'
                                  + gplus_id, 'GET')
        data = json.loads(content)
        email = data["emails"][0]["value"]
        name = data['displayName']
        return signin(email, name)

    except Exception as e:
        print(e)
        return "Error has occurred"


@auth.route('/fakesignin')
def fakesignin():
    # Get params from the request
    parser = reqparse.RequestParser()
    parser.add_argument('Email', type=str, required=True, help='E-mail must be provided.',
                        location='headers')
    parser.add_argument('Name', type=str, required=True, help='Name must be provided.',
                        location='headers')
    args = parser.parse_args()
    return signin(args['Email'], args['Name'])


@auth.route('/fakeregister/<uni>/<name>')
def fakeregister(uni, name):
    user = User(uni, name, 0, 0)
    db.session.add(user)
    db.session.commit()
    return "Registered a fake user."


@auth.route('/rate_user/<user_id>/<rating>')
def rate_user(user_id, rating):
    # Get matching users
    rating = int(rating)
    matching_users = User.query.filter_by(user_id=user_id).all()
    if len(matching_users) == 0:
        return "No matching users found!"
    matching_users[0].num_ratings += 1
    if rating > 0:
        matching_users[0].rating_value += 1
    elif rating < 0:
        matching_users[0].rating_value -= 1
    db.session.commit()

    # Percent formula is here (average is 0.5)
    return "New rating achieved; percent is: " \
           + str(float(matching_users[0].rating_value) / float(2 * matching_users[0].num_ratings) + 0.5)


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