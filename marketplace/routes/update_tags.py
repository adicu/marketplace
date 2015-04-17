from flask import Blueprint
from marketplace import db, login_required
from marketplace.models import Item, Tag

update_tags = Blueprint('update_tags', __name__)


@update_tags.route('/update_tags/<item_id>/<tags>')
@login_required
def update_item_tags(item_id, tags):
    # Get matching item
    matching_items = db.session.query(Item).filter_by(id=item_id).all()
    if len(matching_items) == 0:
        return "No matching items found!"
    if len(matching_items) > 1:
        return "Too many items found!"

    # Remove all current tags from the item; this will update the tag db entry too
    del matching_items[0].tags[:]

    # Get existing item tags and ensure not already there
    for tag in tags:
        # See if the tag is already in the tag database
        tag_t = ""
        matching_tags = db.session.query(Tag).filter_by(name=tag).all()
        if len(matching_tags) == 0:
            # No? Create tag
            tag_t = Tag(tag)
            db.session.add(tag_t)
            db.session.commit()
        else:
            # Add item to new/existing tag
            tag_t = matching_tags[0]

        # Pair up item with tag
        matching_items[0].tags.append(tag_t)
    db.session.commit()

    # For each tag, do some operation
    return "Updated tags!"