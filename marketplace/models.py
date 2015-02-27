from db import Base
from db import db_session

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class User(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    name = Column(String(100), unique=True)
    percent = Column(Integer)


    def __init__(self, user_id, email, name, percent):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.percent = percent


    def __repr__(self):
        return '<User %r>' % self.user_id


class Item(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    item_name = Column(String(200), unique=False)
    item_description = Column(String(2000), unique=False)
    price = Column(Float)


    def __init__(self, user_id, item_name, item_description, price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price


    def __repr__(self):
        return '<Item %r>' % self.item_name