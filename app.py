import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
# This can be any random string for now
app.secret_key = os.getenv("SECRET_KEY")

# db connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False) # this gets hashed before db storage
    
    def __repr__(self):
        return f"<User {self.username}>"

@app.route("/")
def home():
    # check if "user" key exists in the session
    # logged_in = "user" in session
    return render_template("index.html", logged_in="user" in session)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # retreive user in db
        user = User.query.filter_by(username=username).first()
        
        # check if password matches digest
        if user and check_password_hash(user.password_digest, password):
            session["user"] = user.username
            flash(f"Welcome back, {username}!")
            return redirect(url_for("home"))
        else:
            flash(f"Invalid username or password", "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        
        # 1. basic validation
        if password != confirm:
            flash("Passwords do not match!", "error")
            return render_template("signup.html")
        
        # 2. Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already take. Please choose another.", "error")
            return render_template("signup.html")

        # 3. hash the password and save to postgres     
        password_digest = generate_password_hash(password)   
        new_user = User(username=username, email=email, password_digest=password_digest)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "Success")
            return redirect(url_for("home"))
        except Exception as err:
            db.session.rollback()
            flash("An error occured. Please try again.", "error")
            return redirect(url_for("signup"))
        
    return render_template("signup.html")

@app.route("/logout")
def logout():
    # remove user form session
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)