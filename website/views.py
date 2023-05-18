from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Note, Post, Comment
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template("home.html", user=current_user)

    """if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
    
    """
    
@views.route('/download')
@login_required
def download():
    path = 'static\Blast and Dash.zip' # the path of the file to download
    return send_file(path, as_attachment=True) # download the file


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST': 
        submit_button = request.form.get('submit_button')

        if submit_button == 'post_btn':
            post = request.form.get('post')
            title = request.form.get('title')

            if len(post) < 1:
                flash('Post is too short!', category='error') 
            else:
                new_post = Post(content=post, title=title, user_id=current_user.id)  #providing the schema for the post 
                db.session.add(new_post) #adding the post to the database 
                db.session.commit()
                flash('Post added!', category='success')

        elif submit_button == 'comment_btn':
            comment = request.form.get('comment')

            if len(comment) < 1:
                flash('Comment is too short!', category='error') 
            else:
                new_comment = Comment(content=comment, user_id=current_user.id)  #providing the schema for the post 
                db.session.add(new_comment) #adding the comment to the database 
                db.session.commit()
                flash('Comment added!', category='success')

    return render_template('forum.html', user=current_user)

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template('game.html', user=current_user)