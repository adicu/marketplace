from flask import Blueprint
from marketplace import db
from marketplace.models import Item
from datetime import date

insert = Blueprint('insert', __name__) # Leave of URL prefix intentionally


@insert.route('/insert/<user_id>/<name>/<description>/<float:price>')
def insert_item(user_id, name, description, price):
    new_item = Item(user_id, name, description, price, date.today(), date.today(), 'listed')
    db.session.add(new_item)
    db.session.commit()
    return "Item added with id: " + str(new_item.id)


@insert.route('/bulk_test')
def bulk_test():
    for i in range(100):
        new_item = Item("mockuser", "test", "sample", i, date.today(), date.today(), 'listed')
        db.session.add(new_item)
    db.session.commit()
    return "Bulk test complete."