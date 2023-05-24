from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #print(current_user) # print current user for testing purposes
    # Print all data from the Post table for testing purposes
    """users = User.query.all()
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
        print("---")"""

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
    print("Current user" + str(current_user)) #check if current user working

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['post']
        user_name = current_user.first_name

        if len(title) < 1:
            flash('Title is too short!', category='error')

        elif len(content) < 1:
            flash('Post is too short!', category='error')

        else:
            new_post = Post(title=title, content=content, user_id=current_user.id, user_name=user_name)
            db.session.add(new_post)
            db.session.commit()
            flash('Post submitted successfully!', category='success')

    posts = Post.query.all()
    return render_template('forum.html', posts=posts, user=current_user)


@views.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def create_comment(post_id):
    print("Post ID:" + str(post_id)) #check post_id working
    comment_content = request.form['comment']

    if len(comment_content) < 1:
        flash('Comment is too short!', category='error')
    else:
        user_name = current_user.first_name
        new_comment = Comment(content=comment_content, post_id=post_id, user_name=user_name) #providing the schema for the post
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added to post!', category='success')

    return redirect('/forum')

@views.route('/profile')
@login_required
def profile():
    posts = Post.query.all()
    return render_template('profile.html', user=current_user, posts=posts)

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template('game.html', user=current_user)