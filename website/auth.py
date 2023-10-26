from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User # allows us to create user
from . import db # means from __init__.py import db
from werkzeug.security import generate_password_hash, check_password_hash # allows us to hash password, you can see hash of someones password
#but you cant trace that hash to original password, you check hash of original password on register with login hash password if they match
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # data = request.form -- see all the data that user is giving to server
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # look for specific user by email (email=email) filter all users that have this email
        if user: # if user exists
            if check_password_hash(user.password, password): # check if password matches password hash, pass password from form
                flash('You are logged in', category='success') 
                login_user(user, remember=True) # login user, remember=True means user will stay logged in for 30 days, flask session will be updated
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Incorrect email', category='error') # if user not found email does not exist

    return render_template('login.html', user=current_user) # set session for logged in user

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user = User.query.filter_by(email=email).first() # check db for existing email
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        elif password!= confirm:
            flash('Passwords do not match', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index')) # views file home url or just use redirect('/')

    return render_template('register.html', user=current_user)