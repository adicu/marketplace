from flask import Blueprint
from marketplace.models import User

rate_user = Blueprint('rate_user', __name__)


@rate_user.route('/rate_user/<user_id>/<rating>')
def rate_a_user(user_id, rating):
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