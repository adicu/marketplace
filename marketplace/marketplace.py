from flask import Flask, jsonify, render_template, json, request, url_for
from db import db # Import database functions
# this is test
app = Flask(__name__)

import sqlalchemy

# Import configuration from Flask
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0'
)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host=app.config['HOST'])
# comments
