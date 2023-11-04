from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Todo
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def index():
    return render_template("index.html", user=current_user)

@views.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if title and description:
            todo_item = Todo(title=title, description=description, user_id=current_user.id)
            db.session.add(todo_item)
            db.session.commit()
            flash('Todo item added!', category='success')
        else:
            flash('Please provide both a title and description for the todo item.', category='error')

    return render_template("todo.html", user=current_user)

@views.route('/delete-todo', methods=['POST'])
def delete_todo():
    todo = json.loads(request.data) 
    todoId = todo['todoId']
    todo = Todo.query.get(todoId) 
    if todo: 
        if todo.user_id == current_user.id: 
            db.session.delete(todo)
            db.session.commit()
    return jsonify({})

@views.route('/complete-todo', methods=['POST'])
def complete_todo():
    todo = json.loads(request.data) 
    todoId = todo['todoId']
    todo = Todo.query.get(todoId) 
    if todo: 
        if todo.user_id == current_user.id: 
            if todo.completed == False:
                todo.completed = True
                db.session.commit()
            else:
                todo.completed = False
                db.session.commit()
    return jsonify({})

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # load note id from js
    noteId = note['noteId'] # set noteId to be nodeId passed in data
    note = Note.query.get(noteId) # look for note that has that id
    if note: # if note with id exists
        if note.user_id == current_user.id: # if user owns this note
            db.session.delete(note) # delete note
            db.session.commit()
    
    return jsonify({}) # turn empty python dict into json object and return, we have to return something
