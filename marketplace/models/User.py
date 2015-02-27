from flask import url_for
from flask.ext.sqlalchemy import SQLalchemy
from marketplace import db

class User(db.Model):
	class User(Base):
    __tablename__ = 'users'
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