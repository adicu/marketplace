from flask import Blueprint, jsonify, render_template, json, request, redirect, session, url_for
from marketplace import db, flow, login_required
from marketplace.models import User
from marketplace.routes import home
from oauth2client.client import OAuth2WebServerFlow
from datetime import date, datetime
from flask.ext.restful import reqparse  # Parse through requests
import httplib2
import re

auth = Blueprint('auth', __name__)

# From Density project
CU_EMAIL_REGEX = r"^(?P<uni>[a-z\d]+)@.*(columbia|barnard)\.edu$"


@auth.route("/logout")
def logout():
    session.pop("username", None)
    session["logged_in"] = False
    return redirect(url_for('home.home_page'))


@auth.route("/session_test")
def session_test():
    if "username" in session:
        return session["username"]
    else:
        return "You're not logged in."


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
        #home.home_page_error("An error occcurred authenticating you.")
        return redirect(url_for('home.home_page'))
    else:  # We just got to the code in the first place
        return redirect(flow.step1_get_authorize_url())


def signin(email):
    """
    Post Google sign in, register as necessary or just return to listings
    """
    matching_users = User.query.filter_by(user_id=email).all()
    matches = len(matching_users)
    if matches == 0:
        return register(email)
    elif matches == 1:
        session["username"] = matching_users[0].user_id
        session["logged_in"] = True
        return redirect(url_for('home.home_page'))
    #home.home_page_error("Error signing in!")
    return redirect(url_for('home.home_page'))


def register(email):
    """
    Register a new user.
    """
    # Catch regex errors
    regex_result = re.match(CU_EMAIL_REGEX, email)
    if not regex_result:
        return redirect(url_for('home.home_page'))
        #home.home_page_error("Please login with a Columbia or Barnard provided email.")
        return

    user = User(email, 0, 0)
    db.session.add(user)
    db.session.commit()

    session["username"] = email
    session["logged_in"] = True

    return redirect(url_for('home.home_page'))
    #home.home_page_error("Welcome to Marketplace!")