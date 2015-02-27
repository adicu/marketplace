from flask import Flask, jsonify, render_template, json, request


app = Flask(__name__)

import sqlalchemy

# Import configuration from Flask
app.config.update(
	DEBUG=True,
	HOST='0.0.0.0'
)

@app.route('/')
def index():
	return "Marketplace"

@app.route('/auth')
def auth():
	
if __name__ == '__main__':
	app.run(host=app.config['HOST'])