from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') #receives the text from name=email field and stores in variable
        password = request.form.get('password') #receives the text from name=password field and stores in variable

        user = User.query.filter_by(email=email).first() #searches User table for the email provided. Will return first...
        #... match found as there should be no duplicates.
        if user:
            if check_password_hash(user.password, password): #check password correct using password hashes
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #login user and remember them for this session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error') #will flash password error
        else:
            flash('Email does not exist.', category='error') #will flash email error

    return render_template("login.html", user=current_user) 


@auth.route('/logout')
@login_required
def logout():
    logout_user() #logs user out
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email') #receives the text from name=email field and stores in variable
        first_name = request.form.get('firstName') #receives the text from name=firstName field and stores in variable
        password1 = request.form.get('password1') #receives the text from name=password1 field and stores in variable
        password2 = request.form.get('password2') #receives the text from name=password2 field and stores in variable

        user = User.query.filter_by(email=email).first() #query whether the user already exists in DB
        if user:
            flash('Email already exists.', category='error') #flash error if user already exists
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') #email must be longer than 3 character or flash error
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error') #name must be longer than 1 character or flash error
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error') #flash error if password1 and password2 dont match
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error') #password must be atleast 7 characters or flash error
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256')) #prepare to store in DB. Password will store hash of password for security
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

