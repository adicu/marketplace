from flask import Blueprint, render_template

home = Blueprint('name', __name__)


@home.route('/')
def home_page():
    """ Our home page. """
    return render_template('index.html')

@home.route('/login')
def login_page():
    """ Our home page. """
    return render_template('login.html')
