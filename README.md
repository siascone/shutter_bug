# ShutterBug

An app for camera enthusiasts to catalog their cameras and equipment, share 
photos and connect with fellow shutter bugs.

## Tech Stack
- PostgreSQL
- Python/Flask (backend routing)
- JavaScript/React (frontend routing and UI)
- HTML/CSS (display and style)

## Planned Features
- User Authorization - Under Construction
- Home Page (index of user posts)
- Camera Cabinet (index of a user's colleciton of camera/equipent items) 
    - Cabinet item page
- Profile page (index of user's posts and details)
- Posts (users can create, update and delete public photo and text posts) 
- Likes (users can like other users posts)
- Friends (users can be friends with other users)
- Wishlist (users can create a list of items they are looking for)
- Comments (users can comment on posts, and wishlist itemds)

## Getting Started
- set up a virtual env `python -m venv venv`
- give execute permission to venv acticate executable `chmod +x venv/bin/activate`
- start virtual env `. .venv/bin/activate`
- install requirements: (NOTE TO SELF: I need to make a requirements.txt file to run pip installs automatically)
  - install flask `pip install flask`
  - install sqlalchemy `pip install flask-sqlalchemy`
  - install python-postgres driver `pip install psycopg2-binary`
  - install dotenv `pip install python-dotenv`
  - install werkzeug `pip install werkzeug`
- setup flask `. ./setup.snh`
- create `.env` file
  - add a DATABASE_URL="postgresql://my_app_user:secure_password@localhost:5432/my_flask_app
  - add a SECRET_KEY=<large_alnum_string>
- run seeds file `python seed.py`
- run app `flask --app app.py run`

### Local DB setup
- Create a dedicated user for the app `CREATE USER my_app_user WITH PASSWORD 'secure_password';`
- Create the database `CREATE DATABASE my_flask_app;`
- Give all permissions on database to user `GRANT ALL PRIVILEGES ON DATABASE my_flask_app TO my_app_user;`
- Connect to psql my_flask_app and give schema permissions `GRANT ALL ON SCHEMA public TO my_app_user;`

