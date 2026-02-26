from app import app
from dotenv import load_dotenv
from models import db, User, Post
from werkzeug.security import generate_password_hash

load_dotenv()
            
def seed_database():
    with app.app_context():
        print("Connecting to the database...")
        
        print("Dropping tables...")
        db.drop_all()
        print("Tables dropped.")
        
        print("Creating tables...")
        db.create_all()
        print("Tables created.")
        
        print("Seeding database...")
        
        user_seeds = [
            {"username": "shutterbug1", "email": "sb1@shutterbug.com", "password": "password"},
            {"username": "nikon4life", "email": "nikon4life@shutterbug.com", "password": "password"},
            {"username": "canonloverAE1", "email": "canonloverae1@shutterbug.com", "password": "password"}
        ]
        
        users = {}
        for user in user_seeds:
            user_exists = User.query.filter_by(username=user["username"]).first()
            if not user_exists:
                password_digest = generate_password_hash(user["password"])
                new_user = User(
                    username=user["username"],
                    email=user["email"],
                    password_digest=password_digest
                )
                db.session.add(new_user)
                db.session.commit()
                
            users[user["username"]] = new_user
                
        posts = [
            {
                "author": users["shutterbug1"],
                "body": "Golden hour at the pier today! The dynamic range on modern sensors is just cheating at this point. I recovered so much detail from the shadows."
            },
            {
                "author": users["nikon4life"],
                "body": "Just picked up the Noct 58mm f/0.95. The depth of field is so thin I think I accidentally blurred out the subject's personality. Absolute bokeh machine!"
            },
            {
                "author": users["canonloverAE1"],
                "body": "Nothing beats the tactile click of the AE-1 Program. No autofocus, no face-tracking—just you, the light meter, and 36 frames of pure intention."
            },
            {
                "author": users["nikon4life"],
                "body": "The Z-mount transition was scary at first, but the sharpness of these new S-line lenses is undeniable. Sorry F-mount, you served me well."
            },
            {
                "author": users["canonloverAE1"],
                "body": "Unpopular opinion: Film is actually cheaper than digital if you consider that I don't feel the need to buy a new $3,000 body every two years."
            }
        ]
        
        for post in posts:
            if not Post.query.filter_by(body=post["body"]).first():
                new_post = Post(body=post["body"], author=post["author"])
                db.session.add(new_post)
                
        db.session.commit()
        print("Database seeded successfully!")
        
if __name__ == "__main__":
    seed_database()
    
