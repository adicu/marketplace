from flask import Blueprint, request, render_template
from marketplace import db, session, login_required
from marketplace.models import Item
from marketplace.forms import InsertForm
from datetime import date, datetime

insert = Blueprint('insert', __name__) # Leave of URL prefix intentionally


@insert.route('/insert/<name>/<description>/<condition>/<image_url>/<float:price>')
@login_required
def insert_item(name, description, condition, image_url, price):
    new_item = Item(session["username"], name, 
        description, condition, image_url, price, 
        date.today(), date.today(), None, 'listed')
    db.session.add(new_item)
    db.session.commit()
    return "Item added with id: " + str(new_item.id)


@insert.route('/sell_item', methods=['GET', 'POST'])
@login_required
def sell_item():
    form = InsertForm(request.form)
    if request.method == 'POST' and form.validate():
        insert_item(form.name.data, form.description.data,
                    form.condition.data, "boo", form.price.data)
        return "Item added"
    return render_template('sell.html', form=form)


@insert.route('/mark_sold/<item_id>/<sold_to>')
@login_required
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
@login_required
def bulk_test():
    for i in range(100):
        new_item = Item("uni123", "Product name", "Product description", "new"
                        "http://www.dunbartutoring.com/wp-content/themes/thesis/rotator/sample-1.jpg",
                        i, datetime.utcnow(), datetime.utcnow(), None,
                        'listed')
        db.session.add(new_item)
    db.session.commit()
    return "Bulk test complete."