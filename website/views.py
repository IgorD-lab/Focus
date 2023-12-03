from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .models import Note, Todo, Quiz, User, Deck, Flashcard, TempFlashcard
from . import db
import json, random

views = Blueprint('views', __name__)

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

@views.route('/delete-note-all', methods=['POST'])
def delete_note_all():
    user_data = json.loads(request.data)
    user_id = user_data['userId']
    user = User.query.get(user_id)
    if user:
        notes = Note.query.filter_by(user_id=user.id).all()
        for note in notes:
            db.session.delete(note)
        db.session.commit()
    return jsonify({})

# @views.route('/quiz', methods=['GET', 'POST'])
# @login_required
# def quiz():
#    if request.method == 'POST':
#         question = request.form.get('question')
#         answer = request.form.get('answer')
#         if question and answer:
#             quiz_item = Quiz(question=question, answer=answer, user_id=current_user.id)
#             db.session.add(quiz_item)
#             db.session.commit()
#             flash('Quiz item added!', category='success')
#         else:
#             flash('Please provide both a question and answer for the question item.', category='error')

#    return render_template('quiz.html', user=current_user)

# @views.route('/quiz-questions', methods=['GET', 'POST'])
# @login_required
# def quiz_questions():
#     if 'quiz_id' in session:
#         # If quiz_id is in the session, retrieve the question using quiz_id
#         question = Quiz.query.get(session['quiz_id'])
#         if request.method == 'POST':
#             answer = request.form.get('answer').strip().lower()
#             print(f"Database answer: '{question.answer}', User answer: '{answer}'")
#             if question.answer.strip().lower() == answer:
#                 flash('Correct answer', category='success')
#                 print('Correct')
#             else:
#                 flash('Wrong answer', category='error')
#                 print('Error')
#             session.pop('quiz_id', None)
#             # After checking the answer, fetch a new question
#             question = Quiz.query.order_by(func.random()).first()
#             session['quiz_id'] = question.id
#     elif request.method == 'POST':
#         # If quiz_id is not in the session and the form is submitted, fetch a new question
#         question = Quiz.query.order_by(func.random()).first()
#         session['quiz_id'] = question.id
#     else:
#         # If quiz_id is not in the session and the form is not submitted, do nothing
#         question = None

#     return render_template('quiz-questions.html', user=current_user, question=question)

# @views.route('/delete-quiz', methods=['POST'])
# def delete_quiz():
#     quiz = json.loads(request.data) 
#     quizId = quiz['quizId'] 
#     quiz = Quiz.query.get(quizId) 
#     if quiz: 
#         if quiz.user_id == current_user.id: 
#             db.session.delete(quiz) 
#             db.session.commit()
#     return jsonify({})

# @views.route('/delete-quiz-all', methods=['POST'])
# def delete_quiz_all():
#     user_data = json.loads(request.data)
#     user_id = user_data['userId']
#     user = User.query.get(user_id)
#     if user:
#         quizzes = Quiz.query.filter_by(user_id=user.id).all()
#         for quiz in quizzes:
#             db.session.delete(quiz)
#         db.session.commit()
#     return jsonify({})

@views.route('/decks', methods=['GET', 'POST'])
def decks():
    if request.method == 'POST':
        if 'name' in request.form:
            name = request.form['name']
            existing_deck = Deck.query.filter_by(name=name).first()

            if existing_deck is None:
                deck = Deck(name=name)
                db.session.add(deck)
                db.session.commit()
                return redirect('/decks')
            else:
                flash('A deck with that name already exists. Please choose a different name.', 'error')

        if 'question' in request.form and 'answer' in request.form and 'deck_id' in request.form:
            question = request.form['question']
            answer = request.form['answer']
            deck_id = request.form['deck_id']
            flashcard = Flashcard(question=question, answer=answer, deck_id=deck_id)
            db.session.add(flashcard)
            db.session.commit()
            flash('Qestion Added', 'success')

    decks = Deck.query.all()
    return render_template('decks.html', decks=decks, user=current_user)

@views.route('/deck/<int:deck_id>', methods=['GET'])
def deck(deck_id):
   deck = Deck.query.get(deck_id)
   return render_template('deck.html', deck=deck, user=current_user)

@views.route('/delete-deck/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if deck:
        Flashcard.query.filter_by(deck_id=deck_id).delete()
        db.session.delete(deck)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 404

@views.route('/deck-questions/<int:deck_id>', methods=['GET', 'POST'])
def deck_questions(deck_id):
    deck = Deck.query.get(deck_id)
    user_id = current_user.id

    if request.method == 'POST':
        if 'flashcard_id' in session:
            flashcard = Flashcard.query.get(session['flashcard_id'])
            answer = request.form.get('answer').strip().lower()
            print(f"Database question: '{flashcard.question}'")
            print(f"Expected answer: '{flashcard.answer}'")
            print(f"User answer: '{answer}'")
            if answer == flashcard.answer.lower():
                flash('Correct!', category='success')
            else:
                flash(f'Incorrect! The correct answer was: {flashcard.answer}', category='error')

            TempFlashcard.query.filter_by(user_id=user_id, flashcard_id=flashcard.id).delete()
            db.session.commit()

        temp_flashcard = TempFlashcard.query.filter_by(user_id=user_id).first()
        if temp_flashcard:
            flashcard = Flashcard.query.get(temp_flashcard.flashcard_id)
            session['flashcard_id'] = flashcard.id
        else:
            flashcard = None
            flash('You have answered all questions', category='success')
            session.pop('flashcard_id', None)
    else:
        TempFlashcard.query.filter_by(user_id=user_id).delete()
        flashcards = list(deck.flashcards)
        if 'flashcard_id' in session:
            flashcards = [f for f in flashcards if f.id != session['flashcard_id']]
        random.shuffle(flashcards)
        for flashcard in flashcards:
            temp_flashcard = TempFlashcard(user_id=user_id, flashcard_id=flashcard.id)
            db.session.add(temp_flashcard)
        db.session.commit()

        flashcard = Flashcard.query.get(TempFlashcard.query.filter_by(user_id=user_id).first().flashcard_id)

    return render_template('deck_questions.html', flashcard=flashcard, deck=deck,  user=current_user)
