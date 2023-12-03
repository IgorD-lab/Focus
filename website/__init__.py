# __init__ makes folder a python package that can be imported in main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path # for create database
from flask_login import LoginManager


db = SQLAlchemy() # define new database
DB_NAME = 'database.db' # database name

def create_app():
    app = Flask(__name__) # initialise flask
    app.config['SECRET_KEY'] = 'banana' # encrypt cookies and session 
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # tell flask that we are using this db and where db is located
    db.init_app(app) # initialise database tell it that we are going to use app with it
     
    from .views import views #import blueprints
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') #register blueprints
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Todo, Quiz, Deck, Flashcard, TempFlashcard # not actually importing we just declare function prototypes before we create database

    with app.app_context():
        db.create_all() # call function

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # tell flask where to go if not logged in
    login_manager.init_app(app) # initialise login manager

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # tell flask what user we are looking for based on id

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME): # import os for path to determine if path to database model exists or not
        db.create_all(app=app) # if database doesn't exist we create it, tell alchemy for which app we are creating and other app contains SQLALCHEMY_DATABASE_URI
        print('Created database!')
