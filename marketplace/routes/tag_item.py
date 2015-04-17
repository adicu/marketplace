from flask import Blueprint
from marketplace import db, login_required
from marketplace.models import Item, Tag

tag_item = Blueprint('tag_item', __name__)


@tag_item.route('/tag_item/<item_id>/<tag>')
@login_required
def tag_an_item(item_id, tag):
    # Get matching item
    matching_items = db.session.query(Item).filter_by(id=item_id).all()
    if len(matching_items) == 0:
        return "No matching items found!"
    if len(matching_items) > 1:
        return "Too many items found!"

    # Get existing item tags and ensure not already there
    item_tags = matching_items[0].tags
    exists = False
    for existing_tag in item_tags:
        if existing_tag.name == tag:
            exists = True
    if exists:
        return "Already exists!"

    # If not, see if the tag is already in the tag database
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

    return "Added tag!"