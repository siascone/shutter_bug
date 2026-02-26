from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False) # this gets hashed before db storage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # joins posts and users table on user_id
    posts = db.relationship('Post', backref='author', lazy=True) # must use model name not table name
    
    def __repr__(self):
        return f"<User {self.username}>"