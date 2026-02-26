import os
from dotenv import load_dotenv
from flask import Flask
from models import db
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.post_routes import posts_bp

# >>> APP/ENV/DB SETUP <<<

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# db connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Call in Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)

if __name__ == "__main__":
    app.run(debug=True)