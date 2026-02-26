from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Post, User
from utils.auth import required_logged_in

posts_bp = Blueprint('posts', __name__)

@posts_bp.route("/posts")
def post_index():
    # get all posts from db ordered by mostrecent created date
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("post_index.html", posts=all_posts)

@posts_bp.route('/posts/new')
@required_logged_in
def create_post():
    if request.method == "POST":
        body = request.form.get("body")
        
        current_user = User.query.filter_by(username=session['user']).first()
        
        new_post = Post(body=body, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        
        flash("Post created!", "success")
        return redirect(url_for("posts.post_view", post_id=new_post.id))
    
    return render_template("create_post.html")

@posts_bp.route("/posts/<int:post_id>")
def post_view(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_view.html", post=post)

@posts_bp.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@required_logged_in
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.username != session['user']:
        flash("You cannot edit someone else's post!", "error")
        return redirect(url_for('posts.post_view', post_id=post_id))
    
    if request.method == "POST":
        post.body = request.form.get("body")
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for('posts.post_view', post_id=post.id))
    
    return render_template("edit_post.html", post=post)

@posts_bp.route("/posts/<int:post_id>/delete", methods=["POST"])
@required_logged_in
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author.username != session['user']:
        flash("You cannot delete someone else's post!", "error")
        return redirect('post_view', post_id=post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "success")
    return redirect(url_for("posts.post_index"))
