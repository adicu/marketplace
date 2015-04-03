from marketplace import db
from marketplace.models import Tag
from marketplace.models import item_tags

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    item_name = db.Column(db.String(200))
    item_description = db.Column(db.String(2000))
    price = db.Column(db.Float)
    date_listed = db.Column(db.Date)
    date_sold = db.Column(db.Date)
    status = db.Column(db.String(20))

    # Reference to the tags table
    tags = db.relationship('Tag', secondary=item_tags, backref=db.backref('items', lazy='dynamic'))

    def __init__(self, user_id, item_name, item_description, price, date_listed, date_sold, status):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price
        self.date_listed = date_listed
        self.date_sold = date_sold
        self.status = status

    def __repr__(self):
        return '<Item %r>' % self.item_name

    @property
    def serialize(self):
        """ Used for JSONify and render templates """
        tag_output = []
        for tag in self.tags:
            tag_output.append(tag.serialize)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'price': self.price,
            'tags': tag_output,
            'date_listed': str(self.date_listed),
            'date_sold': str(self.date_sold),
            'status': self.status
        }