from flask import Blueprint, jsonify, render_template, json, request, redirect
from marketplace import db, flow
from marketplace.models import User
from oauth2client.client import OAuth2WebServerFlow
from datetime import date, datetime
from flask.ext.restful import reqparse  # Parse through requests
import httplib2
import re

auth = Blueprint('auth', __name__)

# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"


@auth.route("/login/google")
def google_login():
    code = request.args.get('code', '')
    error = request.args.get('error', '')
    if code:  # We have a login code
        credentials = flow.step2_exchange(code)
        http = httplib2.Http()
        http = credentials.authorize(http)
        gplus_id = credentials.id_token['sub']
        h, content = http.request('https://www.googleapis.com/plus/v1/people/'
                                  + gplus_id, 'GET')
        data = json.loads(content)
        email = data["emails"][0]["value"]
        return signin(email)
    elif error:  # Google login returned an error; alert the user
        return error
    else:  # We just got to the code in the first place
        return redirect(flow.step1_get_authorize_url())


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


def signin(email):
    """
    Post Google sign in, register as necessary or just return to listings
    """
    matching_users = User.query.filter_by(user_id=email).all()
    matches = len(matching_users)
    if matches == 0:
        return register(email)
    elif matches == 1:
        return jsonify(data=[user.serialize for user in matching_users])
    return "Error!"


def register(email):
    """
    Register a new user.
    """
    try:
        # Catch regex
        regex_result = re.match(CU_EMAIL_REGEX, email)
        if not regex_result:
            raise NameError("Invalid e-mail")

        user = User(email, 50.0, 0)
        db.session.add(user)
        db.session.commit()
        return "Welcome to Marketplace!"
    except Exception:
        return "We couldn't register you. Make sure you use a Columbia or Barnard email."