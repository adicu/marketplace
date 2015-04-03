from marketplace import db

# Association table for associating items with tags and vice-versa
item_tags = db.Table('item_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)

from marketplace.models.user import User
from marketplace.models.tag import Tag  # Must come before Item, because Item refers to Tag for the relationship
from marketplace.models.item import Item
