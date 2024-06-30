from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .models import Note, Todo, User, Deck, Flashcard
from . import db
import json, random

views = Blueprint('views', __name__)

@views.app_context_processor
def inject_user():
    return dict(user=current_user)

@views.route('/', methods=['GET'])
@login_required
def index():
    return render_template("index.html", user=current_user)

@views.route('/timer', methods=['GET'])
@login_required
def timer():
    return render_template("timer.html", user=current_user)

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
        title = request.form.get('noteTitle')
        description = request.form.get('noteDescription')
        if not title or not description:
            flash('Please fill in both title and description.', category='error')
        else:
            new_note = Note(title=title, data=description, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        # Redirect to the same endpoint to refresh the page and fetch updated list of notes
        return redirect(url_for('views.notes'))

    # Fetch notes after handling POST to ensure the list includes any newly added notes
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", user=current_user, notes=notes)


@views.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:  # Ensure that the current user owns the note
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
        else:
            flash('You do not have permission to delete this note.', category='error')
    else:
        flash('Note not found.', category='error')
    
    return redirect(url_for('views.notes'))


@views.route('/edit-note/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        title = request.form.get('noteTitle')
        description = request.form.get('noteDescription')
        if title:
            note.title = title
        if description:
            note.data = description
        db.session.commit()
        flash('Note updated successfully!', 'success')
    else:
        flash('Note not found or you do not have permission to edit this note.', 'error')
    return redirect(url_for('views.notes'))


@views.route('/study-decks', methods=['GET'])
@login_required
def study_decks():
    decks = Deck.query.filter_by(user_id=current_user.id).all()
    return render_template('decks/study_decks.html', decks=decks)

@views.route('/study-decks/new', methods=['GET', 'POST'])
@login_required
def new_deck():
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_deck = Deck(title=title, user_id=current_user.id)
            db.session.add(new_deck)
            db.session.commit()
            flash('New deck created!', category='success')
            return redirect(url_for('views.study_decks'))
    return render_template('decks/new_deck.html')

@views.route('/study-decks/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        if question and answer:
            flashcard = Flashcard(question=question, answer=answer, deck_id=deck.id)
            db.session.add(flashcard)
            db.session.commit()
            flash('Flashcard added!', category='success')
    flashcards = Flashcard.query.filter_by(deck_id=deck.id).all()
    return render_template('decks/view_deck.html', deck=deck, flashcards=flashcards)

@views.route('/study-decks/<int:deck_id>/quiz', methods=['GET'])
@login_required
def start_quiz(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    flashcards = Flashcard.query.filter_by(deck_id=deck.id).all()
    if flashcards:
        random.shuffle(flashcards)
    return render_template('decks/start_quiz.html', flashcards=flashcards)


