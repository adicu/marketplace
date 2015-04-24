from flask import Blueprint
from marketplace import db, login_required, session
from marketplace.models import User, Item

rate_user = Blueprint('rate_user', __name__)


@rate_user.route('/rate_user/<user_id>/<item_id>/<rating>')
@login_required
def rate_a_user(user_id, item_id, rating):
    # Get matching users
    rating = int(rating)
    matching_users = User.query.filter_by(user_id=user_id).all()
    if len(matching_users) == 0:
        return "No matching users found!"

    # Query the object, and verify properties
    matching_items = Item.query.filter_by(id=item_id).filter_by(user_id=user_id).all()
    if len(matching_items) == 0:
        return "No matching items found!"
    if matching_items[0].status != "sold":
        return "You can't rate a seller on an item with status " + matching_items[0].status + "."
    if matching_items[0].sold_to != session["username"]:
        return "You can't rate a seller on an item that wasn't sold to you!"

    matching_items[0].status = "rated"
    matching_users[0].num_ratings += 1
    if rating > 0:
        matching_users[0].rating_value += 1
    elif rating < 0:
        matching_users[0].rating_value -= 1
    db.session.commit()

    # Percent formula is here (average is 0.5)
    return "New rating achieved; percent is: " \
           + str(calculate_rating(matching_users[0].rating_value, 
                 matching_users[0].num_ratings))


@rate_user.route('/user_rating/<user_id>')
@login_required
def user_rating(user_id):
    matching_users = User.query.filter_by(user_id=user_id).all()
    if len(matching_users) == 0:
        return "No matching users found!"
    else:
        return "Rating is: " \
           + str(calculate_rating(matching_users[0].rating_value, 
                 matching_users[0].num_ratings))


def calculate_rating(rating_value, num_ratings):
    if num_ratings == 0:
        return 0.5
    diff = (float(rating_value) / float(num_ratings)) / 2 # Max/min = 0.5/-0.5
    return diff + 0.5