from flask import Blueprint
from marketplace import db, session
from marketplace.models import Item
from datetime import date, datetime

insert = Blueprint('insert', __name__) # Leave of URL prefix intentionally


@insert.route('/insert/<user_id>/<name>/<description>/<image_url>/<float:price>')
def insert_item(user_id, name, description, image_url, price):
    new_item = Item(user_id, name, description, image_url, price, date.today(), date.today(), None, 'listed')
    db.session.add(new_item)
    db.session.commit()
    return "Item added with id: " + str(new_item.id)


@insert.route('/mark_sold/<item_id>/<sold_to>')
def mark_sold(item_id, sold_to):
    item = Item.query.filter_by(id=item_id).all()
    if len(item) == 0:
        return "No item found!"
    if item[0].user_id != session["username"]:
        return "You can't mark someone else's item as sold. Bad."
    if item[0].status != "listed":
        return "You can't mark this item as sold. It's in state " + item[0].status + "."
    if sold_to == session["username"]:
        return "You can't sell an item to yourself."
    item[0].status = "sold"
    item[0].sold_to = sold_to
    db.session.commit()
    return "Marked as sold."


@insert.route('/bulk_test')
def bulk_test():
    for i in range(100):
        new_item = Item("uni123", "Product name", "Product description",
                        "http://www.dunbartutoring.com/wp-content/themes/thesis/rotator/sample-1.jpg",
                        i, datetime.utcnow(), datetime.utcnow(), None,
                        'listed')
        db.session.add(new_item)
    db.session.commit()
    return "Bulk test complete."