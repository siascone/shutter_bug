from app import app, db, User
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        # clear existing tables
        
        print("Dropping tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        
        print("Seeding database...")
        
        users = [
            {"username": "shutterbug1", "email": "sb1@shutterbug.com", "password": "password"},
            {"username": "nikon4life", "email": "nikon4life@shutterbug.com", "password": "password"},
            {"username": "canonloverAE1", "email": "canonloverae1@shutterbug.com", "password": "password"}
        ]
        
        for user in users:
            if not User.query.filter_by(username=user["username"]).first():
                password_digest = generate_password_hash(user["password"])
                new_user = User(
                    username=user["username"],
                    email=user["email"],
                    password_digest=password_digest
                )
                db.session.add(new_user)
                
        db.session.commit()
        print("Database seeded successfully!")
        
if __name__ == "__main__":
    seed_database()
    
