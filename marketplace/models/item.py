from marketplace import db
from marketplace.models import Tag
from marketplace.models import item_tags

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    item_name = db.Column(db.String(200))
    item_description = db.Column(db.String(2000))
    image_url = db.Column(db.String)
    price = db.Column(db.Float)
    date_listed = db.Column(db.DateTime)
    date_sold = db.Column(db.DateTime)
    sold_to = db.Column(db.String(100))
    status = db.Column(db.String(20))

    # Reference to the tags table
    tags = db.relationship('Tag', secondary=item_tags, backref=db.backref('items', lazy='dynamic'))

    def __init__(self, user_id, item_name, item_description, item_url, price, date_listed, date_sold, sold_to, status):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.image_url = item_url
        self.price = price
        self.date_listed = date_listed
        self.date_sold = date_sold
        self.sold_to = sold_to
        self.status = status

        # User ID:
        # -- The user who is selling the item. (e.g. uni123@columbia.edu)
        # Item name: 
        # -- The name of the item. (e.g. "Old Sofa")
        # Item description:
        # -- A description of the item. (e.g. "A sofa. It's old.")
        # Image URL:
        # -- An image for the item. Ideally hosted on our server, and uploaded from forms.
        # -- (e.g. "http://marketplace.adicu.com/imgs/old_sofa.jpg")
        # Price:
        # -- How much the item costs. It's a float. (e.g. 50.00)
        # Date Listed:
        # -- When the item was listed for sale on the website. (e.g. [some date])
        # Date Sold:
        # -- When the item was sold on the website. (e.g. [some date])
        # Sold To:
        # -- The user who the item was sold to. This will often be None, because the item
        #    hasn't been sold yet. (e.g. mgb123@columbia.edu)
        # Description of status values:
        # -- listed: The item is listed, and visible on the website.
        # -- sold: The item has been sold, but the seller hasn't been rated.
        # -- rated: The item has been sold, and the seller has been rated.
        # -- deleted: The item has been deleted, and is pending deletion
        # -- [anything else]: Invalid field name. Bad. 
        # -- (e.g. "listed")

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
            'item_url': self.image_url,
            'price': self.price,
            'tags': tag_output,
            'date_listed': str(self.date_listed),
            'date_sold': str(self.date_sold),
            'status': self.status
        }