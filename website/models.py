from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

#Database tables
  
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    content= db.Column(db.String(10000))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(30))
    #user = relationship('User', backref='comments')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    title= db.Column(db.String(100))
    sub_title= db.Column(db.String(1000))
    content= db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', backref='posts')
    user_name = db.Column(db.String(30))
    comments = db.relationship('Comment', backref='post', lazy='dynamic') #relationship with comment table 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #posts = db.relationship('Post')
    #comments = db.relationship('Comment')