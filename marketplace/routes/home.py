from flask import Blueprint, Flask, g, jsonify, render_template, json, request, url_for

home = Blueprint('name', __name__)


@home.route('/')
def home_page():
    """ Our home page. """
    return render_template('index.html')


@home.route('/list')
def list_page():
    return render_template('itemList.html')

@home.route('/details')
def details_page():
    return render_template('details.html')

@home.route('/sell')
def sell_page():
    return render_template('sell.html')