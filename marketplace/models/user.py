from marketplace import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True)
    rating_value = db.Column(db.Integer)
    num_ratings = db.Column(db.Integer)

    def __init__(self, user_id, rating_value, num_ratings):
        self.user_id = user_id
        self.rating_value = rating_value
        self.num_ratings = num_ratings

    def __repr__(self):
        return '<User %r>' % self.user_id

    @property
    def serialize(self):
        """ Used for JSONify and render templates """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rating_value': self.rating_value,
            'num_ratings': self.num_ratings
        }