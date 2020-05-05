import os
import requests
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
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

class Book():
    """docstring for book"""
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.review = []
class Review(object):
     """docstring for Review"""
     def __init__(self, isbn, rating, review, username):
         self.username = username
         self.rating = rating
         self.review = review
         self.isbn = isbn
                                  
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
    try:
        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",{"username": username, "email": email, "password": hash})
    except:
        flash("that username already exists")
        return render_template("register.html", message="that username already exists")
    else:
        db.commit()
        flash("Register successful")
        session["logged_in"] = True
        session['username'] = username
        return render_template("index.html")

    return
    

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
        session["username"] = username
        flash("Logged in successful")
        return redirect(url_for('index'), "303")
    else:
        flash("Invalid password")
        return redirect(url_for('welcome'), "303")

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session.pop('username', None)
    flash("Logout successful")
    return redirect("http://127.0.0.1:5000")

@app.route('/search', methods=["POST","GET"])
def search():
    search = request.form.get("search").lower()
    results = db.execute(
                "SELECT * FROM books WHERE LOWER(isbn) LIKE :search OR LOWER(title) LIKE :search OR LOWER(author) LIKE :search ORDER BY title",
                {"search": '%' + search + '%'}).fetchall()  
    if results is None:
        return render_template("error.html", message="No such book.")
    else:
        books = []
        for book in results:
            new_book = Book(book.isbn, book.title, book.author, book.year)
            books.append(new_book)
            # return results
        return render_template('index.html', books=books)
        
@app.route('/book/<string:isbn>', methods=["POST", "GET"])
def book(isbn):
    if not session.get("logged_in"):
        flash("You are not logged in")
        return redirect(url_for('index'), "303")
    review_array =[]
    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
    results = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    for review in reviews:
        new_review = Review(review.isbn, review.rating, review.review, review.username)
        review_array.insert(0,new_review)
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "lTA17O0ICb23S8LkAwHWQ", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    goodreads_rating = data["books"][0]['average_rating']
    goodreads_rating_count = data["books"][0]['work_ratings_count']
    
    return render_template("book.html", book=results, comments=review_array, goodreads_rating=goodreads_rating, goodreads_rating_count=goodreads_rating_count)

@app.route('/<string:isbn>', methods=["POST"])
def review(isbn):
    if not session.get("logged_in"):
        flash("You are not logged in")
        return redirect(url_for('index'), "303")
    else:
        user_id = session["username"]
        book_id = isbn
        rating = request.form.get("star")
        review = request.form.get("review")
        message = ""
        display_message = False
        test = []
        try:
            test = db.execute("SELECT username FROM reviews WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
            if user_id in test:
                message="sorry you have already reviewed this book :("
                display_message=True 
        except:
            try:
                db.execute("INSERT INTO reviews (isbn, review, username, rating) VALUES ( :isbn, :review, :username, :rating)", {"isbn": isbn, "review": review, "username": user_id, "rating": rating})
                db.commit()
                return redirect(url_for('book', isbn=isbn, message="message", display_message="display_message"), "303")
            except:
                message="please enter a rating and comment"
                display_message=True
        
        return redirect(url_for('book', isbn=isbn, message="message", display_message="display_message"), "303")

@app.route('/api/<string:isbn>')
def api(isbn):
    res = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "lTA17O0ICb23S8LkAwHWQ", "isbns": isbn})
    
    if res is None:
        return jsonify(
            {
                "error_code": 404,
                "error_message": "Not Found"
            }
        ), 404
    data = goodreads.json()
    goodreads_rating = data["books"][0]['average_rating']
    goodreads_rating_count = data["books"][0]['work_ratings_count']
    book = Book(res.isbn, res.title, res.author, res.year)
    result = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": goodreads_rating_count,
        "average_score": goodreads_rating
    }
    return jsonify(result)
    
    
    
