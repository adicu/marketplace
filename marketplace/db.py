from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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
    user_id = Column(String(100))
    item_name = Column(String(200))
    item_description = Column(String(2000))
    price = Column(Float)


    def __init__(self, user_id, item_name, item_description, price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price


    def __repr__(self):
        return '<Item %r>' % self.item_name