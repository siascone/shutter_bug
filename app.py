import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User, Post

# >>> APP/ENV/DB SETUP <<<

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# db connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# >>> ROUTE PROTECTION <<< (figure out how to decouple from app.py)

def required_logged_in(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        # Check if the 'user' key exits in session
        if "user" not in session:
            flash("You must be logged in to access that page.", "error")
            return redirect(url_for("login"))

        # Otherwise user must be logged in, grant access
        return f(*args, **kwargs)

    return deco_func

def required_logged_out(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        # check if the 'user' key exists in session
        if "user" in session:
            flash("You must be logged out to access that page.", "error")
            return(redirect(url_for("home")))
        
        # otherwise user must be logged out, grant access (signup/login only)
        return f(*args, **kwargs)
    
    return deco_func

# >>> ROUTES <<< (figure out how to decouple from app.py)

@app.route("/")
def home():
    # check if "user" key exists in the session
    # logged_in = "user" in session
    return render_template("index.html", logged_in="user" in session)

@app.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("home"))
        else:
            flash(f"Invalid username or password", "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("home"))
        except Exception as err:
            db.session.rollback()
            flash("An error occured. Please try again.", "error")
            return redirect(url_for("signup"))
        
    return render_template("signup.html")

@app.route("/logout", methods=["POST"])
@required_logged_in
def logout():
    # remove user form session
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))

@app.route("/posts")
def post_index():
    # get all posts from db ordered by mostrecent created date
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("post_index.html", posts=all_posts)

@app.route("/posts/new", methods=["GET", "POST"])
@required_logged_in
def create_post():
    if request.method == "POST":
        body = request.form.get("body")
        
        current_user = User.query.filter_by(username=session['user']).first()
        
        new_post = Post(body=body, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        
        flash("Post created!", "success")
        return redirect(url_for("post_view", post_id=new_post.id))
    
    return render_template("create_post.html")

@app.route("/posts/<int:post_id>")
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_view.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@required_logged_in
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.username != session['user']:
        flash("You cannot edit someone else's post!", "error")
        return redirect(url_for('post_view', post_id=post_id))
    
    if request.method == "POST":
        post.body = request.form.get("body")
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for('post_view', post_id=post.id))
    
    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@required_logged_in
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.username != session['user']:
        flash("You cannot delete someone else's post!", "error")
        return redirect('post_view', post_id=post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "success")
    return redirect(url_for("post_index"))



if __name__ == "__main__":
    app.run(debug=True)