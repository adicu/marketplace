from marketplace import db

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    item_name = Column(String(200), unique=True)
    item_description = Column(String(2000), unique=True)
    price = Column(Float)


    def __init__(self, user_id, item_name, item_description, price):
        self.user_id = user_id
        self.item_name = item_name
        self.item_description = item_description
        self.price = price


    def __repr__(self):
        return '<Item %r>' % self.item_name