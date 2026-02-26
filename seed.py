from app import app
from dotenv import load_dotenv
from models import db, User, Post, Comment
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
                
        posts_seeds = [
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

        posts = []
        for post in posts_seeds:
            if not Post.query.filter_by(body=post["body"]).first():
                new_post = Post(body=post["body"], author=post["author"])
                db.session.add(new_post)
                posts.append(new_post)

        db.session.commit()
        
        comment_seeds = [
            # Comments on Shutterbug1's Golden Hour post (posts[0])
            {
                "commenter": users["nikon4life"],
                "original_post": posts[0],
                "body": "Modern sensors really are magic. My Z9 can practically see in the dark!"
            },
            # Comments on nikon4life's Noct post (posts[1])
            {
                "commenter": users["shutterbug1"],
                "original_post": posts[1],
                "body": "f/0.95 is wild. Do you even have a focus plane at that point, or is it just a focus 'molecule'?"
            },
            {
                "commenter": users["canonloverAE1"],
                "original_post": posts[1],
                "body": "It's a beautiful lens, but I'll stick to my manual FD glass. Much more character."
            },
            # Comments on canonloverAE1's AE-1 post (posts[2])
            {
                "commenter": users["shutterbug1"],
                "original_post": posts[2],
                "body": "The AE-1 is a classic! There’s nothing like the smell of a fresh roll of Portra 400."
            },
            # Comments on canonloverAE1's "Film is cheaper" post (posts[4])
            {
                "commenter": users["nikon4life"],
                "original_post": posts[4],
                "body": "Until you factor in the cost of scanning and the stress of airport X-ray machines! 😂"
            },
            {
                "commenter": users["canonloverAE1"],
                "original_post": posts[4],
                "body": "That's why I develop at home! Darkroom life is the best life."
            }
        ]
        
        for comment in comment_seeds:
            new_comment = Comment(body=comment['body'], commenter=comment["commenter"], original_post=comment["original_post"])
            db.session.add(new_comment)
        
        db.session.commit()
        print("Database seeded successfully!")
        
        
        
if __name__ == "__main__":
    seed_database()
    
