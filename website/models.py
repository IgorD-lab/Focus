#database schema
from . import db 
#. -> from this package (website) if it was outside of website -> from website import db
from flask_login import UserMixin # helps with user object, allows us to see information about currently logged in user
from sqlalchemy.sql import func


class User(db.Model, UserMixin): # UserMixin must be inherited in User object to use flask_login
    id = db.Column(db.Integer, primary_key=True) # Unique integer that defines user member
    email = db.Column(db.String(150), unique=True) # string size must be defined, 2 users cant have same email
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    notes = db.relationship('Note') # connect user with their notes, we can access all the notes user created with this column, 
    # Note for relationship in sql if it was foreign key we would use note lowercase (dumb design)
    todo= db.relationship('Todo')
    quiz = db.relationship('Quiz')
class Note(db.Model): # db.Model tells db that all notes must have below values
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) # max size of note
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # date the note was created, stores time zone information default value is current time,(func just gets current date time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # reference column of another database, stores integer so db.Integer,
    # db.ForeignKey means we must pass id of existing user when we create note object (one to many relationship), one user has many notes,
    # lower case user because User in sql is seen as user and .id for id of user .email would be if we connected them by user email
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class Quiz(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(200), nullable=False)
   answer = db.Column(db.String(200), nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class Deck(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(80), unique=True, nullable=False)
   flashcards = db.relationship('Flashcard', backref='deck', lazy=True)
class Flashcard(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   question = db.Column(db.String(120), nullable=False)
   answer = db.Column(db.String(120), nullable=False)
   deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
class TempFlashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcard.id'))