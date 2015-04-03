# Core application logic
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    HOST='0.0.0.0',
    SQLALCHEMY_DATABASE_URI='sqlite:////home/vagrant/marketplace_db.db'
)

# Create the database object, which we use in the models below
db = SQLAlchemy(app)

# Register our routes
from marketplace.routes.home import home
app.register_blueprint(home)

from marketplace.routes.auth import auth
app.register_blueprint(auth)

from marketplace.routes.insert import insert
app.register_blueprint(insert)

from marketplace.routes.listings import listings
app.register_blueprint(listings)

from marketplace.routes.rate_user import rate_user
app.register_blueprint(rate_user)

from marketplace.routes.tag_item import tag_item
app.register_blueprint(tag_item)

from marketplace.routes.update_tags import update_tags
app.register_blueprint(update_tags)

db.create_all()