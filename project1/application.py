import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	if not session.get("logged_in"):
		return render_template("welcome.html")
	else:
		return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
	username = str(request.form.get("username"))
	password = str(request.form.get("password"))
	email = str(request.form.get("email"))
	# if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
	#   return render_template("error.html", message="No such flight with that id.")
	hash = pbkdf2_sha256.hash(password)
	db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
			   {"username": username, "email": email, "password": hash})
	db.commit()
	flash("Register successful")
	return render_template("index.html")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
	username = str(request.form.get("username"))
	password = str(request.form.get("password"))
	db_hash = db.execute("SELECT password FROM users WHERE username LIKE :name", {"name": username}).fetchone()
	print(db_hash)
	if not db_hash:
		flash("User not found")
		return redirect(url_for('login'), "303")

	db_hash = db_hash[0].encode("utf-8")
	if pbkdf2_sha256.verify(password, db_hash):
		session["logged_in"] = True
		flash("Logged in successful")
		return redirect(url_for('index'), "303")
	else:
		flash("Invalid password")
		return redirect(url_for('welcome'), "303")

