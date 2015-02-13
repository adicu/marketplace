from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

app.config['DEBUG'] = True

PAGE_NOT_FOUND=404


@app.route('/upload', methods=["GET","POST"])
def upload():
	if request.method == "POST":
		item_name=request.form["itemname"]
		price=request.form["price"]
		db = MySQLdb.connect(host="localhost", user="root", passwd="", db="")
		cur = db.cursor() 
		cur.execute("INSERT INTO items VALUES(%s,%s,%d)",(,itemname,price))
		return render_template('profile.html')
	else: #request.method=="GET"
		return render_template('profile.html')
	

@app.route('/profile')
def profile():
	return render_template("profile.html") 


@app.route('/buy')
def buy():
	return render_template("buy.html") 

@app.errorhandler(PAGE_NOT_FOUND)
def not_found(error):
	return ("Sorry, page not found!"), PAGE_NOT_FOUND

@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0")