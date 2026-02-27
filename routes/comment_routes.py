from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Post, User, Comment
from utils.auth import required_logged_in

comments_bp = Blueprint('comments', __name__)

@comments_bp.route("/comments/new", methods=["POST"])
@required_logged_in
def create_comment():
    if request.method == "POST":
        body = request.form.get("body")
        post_id = request.form.get("post_id")
        
        current_user = User.query.filter_by(username=session['user']).first()
        
        new_comment = Comment(body=body, post_id=post_id, commenter=current_user)
        db.session.add(new_comment)
        db.session.commit()
        
        flash("Comment made!", "success")
    else:
        flash("Uh Oh! Looks like something went wrong. Please try again.", "error")
        
    return redirect(url_for("posts.post_view", post_id=post_id))

@comments_bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@required_logged_in
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    print(comment.commenter.username)
    print(session['user'])
    
    if comment.commenter.username != session['user']:
        flash("You cannot delete someone else's comment!", "error")
        return redirect(url_for('posts.post_view', post_id=comment.post_id))
    
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "success")
    return redirect(url_for('posts.post_view', post_id=comment.post_id))
    
    