from flask import Blueprint, jsonify
from marketplace.models.item import Item

listings = Blueprint('listings', __name__)


@listings.route('/listings')
def show_listings():
    items = Item.query.all()
    return jsonify(data=[item.serialize for item in items])
    # return render_template('primary_user_interface.html', data=[item.serialize for item in items])