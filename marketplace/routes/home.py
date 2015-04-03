from flask import Blueprint

home = Blueprint('name', __name__)


@home.route('/')
def home_page():
    """ Our home page. """
    return "In progress"