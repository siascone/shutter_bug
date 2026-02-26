from functools import wraps
from flask import session, redirect, url_for, flash

def required_logged_in(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        # Check if the 'user' key exits in session
        if "user" not in session:
            flash("You must be logged in to access that page.", "error")
            return redirect(url_for("auth.login"))

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