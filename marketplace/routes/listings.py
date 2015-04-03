from flask import Blueprint, jsonify
from marketplace.models.item import Item, Tag
from marketplace import db

listings = Blueprint('listings', __name__)

# Maximum number of entries to return per page
LIMIT = 50


@listings.route('/listings/<offset>')
def show_listings(offset):
    """
    Show every listing on the site. Mostly for debug purposes.

    @param offset: Offset of the entries.
    @return: Up to LIMIT listings in JSON.
    """
    items = Item.query.filter(Item.status == "listed").order_by(Item.date_listed).offset(offset).limit(LIMIT).all()
    return jsonify(data=[item.serialize for item in items])
    # return render_template('primary_user_interface.html', data=[item.serialize for item in items])


@listings.route('/search_listings/<query>/<offset>')
def search_listings(query, offset):
    """
    Search every listing by a given query. We search name, description, and tag name. Performance might be an issue
    on large data sets.

    @param query: Query.
    @param offset: Offset of the entries.
    @return: The results in JSON.
    """
    # Query by tags that contain the query
    tag_subquery = db.session.query(Tag).filter(Tag.name.contains(query)).subquery()
    tag_query_items = db.session.query(Item).join(tag_subquery, Item.tags).all()
    # Query for items that contain the query in the title
    name_query = db.session.query(Item).filter(Item.item_name.contains(query)).all()
    # Query for items that contain the query in the description
    description_query = db.session.query(Item).filter(Item.item_description.contains(query)).all()

    # Merge the 3 lists
    complete_list = list(set(tag_query_items + name_query + description_query))

    # Sort the 3 lists
    complete_list.sort(key=lambda item: item.date_listed, reverse=True)

    # Select by offset and limit
    limit_amount = int(offset) + LIMIT
    if limit_amount > len(complete_list):
        limit_amount = len(complete_list)
    complete_list = complete_list[int(offset):limit_amount]

    return jsonify(data=[item.serialize for item in complete_list])


@listings.route('/listings/<tag_name>/<offset>')
def listings_by_tag(tag_name, offset):
    """
    Show listings that exactly match a given tag (e.g. all textbooks from "textbook" tag).

    @param tag_name: The tag to query by.
    @param offset: The offset of the listings.
    @return: Every listing that matches the tag (in JSON).
    """
    # Query by tag name by first querying matching tags, and then selecting the items with those tags
    tag_subquery = db.session.query(Tag).filter(Tag.name == tag_name).subquery()
    items = db.session.query(Item).join(tag_subquery, Item.tags).offset(offset).limit(LIMIT).all()
    return jsonify(data=[item.serialize for item in items])