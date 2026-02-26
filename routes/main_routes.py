from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    # check if "user" key exists in the session
    # logged_in = "user" in session
    return render_template("index.html", logged_in="user" in session)