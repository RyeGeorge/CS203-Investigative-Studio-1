from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Print all data from the Post table
    users = User.query.all()
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.first_name}")
        print("---")

    # Print all data from the Post table
    posts = Post.query.all()
    for post in posts:
        print(f"Post ID: {post.id}")
        print(f"Title: {post.title}")
        print(f"Content: {post.content}")
        print("---")

    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template("home.html", user=current_user)

    
@views.route('/download')
@login_required
def download():
    path = 'static\Blast and Dash.zip' # the path of the file to download
    return send_file(path, as_attachment=True) # download the file

@views.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['post']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.all()
    return render_template('forum.html', posts=posts, user=current_user)
""" if request.method == 'POST': 
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
            post_id = Post.id

            if len(comment) < 1:
                flash('Comment is too short!', category='error') 
            else:
                new_comment = Comment(content=comment, user_id=current_user.id, post_id=post_id)  #providing the schema for the post 
                db.session.add(new_comment) #adding the comment to the database 
                db.session.commit()
                flash('Comment added!', category='success')

    return render_template('forum.html', user=current_user)"""


"""@views.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def create_comment(post_id):
    comment_content = request.form['comment']
    post = Post.query.get(post_id)
    new_comment = Comment(content=comment_content, post=post, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect('/forum', user=current_user)"""

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template('game.html', user=current_user)