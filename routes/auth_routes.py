from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from utils.auth import required_logged_in, required_logged_out
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
@required_logged_out
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
            return redirect(url_for("main.home"))
        else:
            flash(f"Invalid username or password", "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
@required_logged_out
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
            return redirect(url_for("main.home"))
        except Exception as err:
            db.session.rollback()
            flash("An error occured. Please try again.", "error")
            return redirect(url_for("signup"))
        
    return render_template("signup.html")

@auth_bp.route("/logout", methods=["POST"])
@required_logged_in
def logout():
    # remove user form session
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("main.home"))

