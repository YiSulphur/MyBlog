from datetime import datetime
from MyBlog import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',back_populates='posts')
    comments = db.relationship('Comment',back_populates='post')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow, index = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='comments')
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates='comments')

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',back_populates = 'author')
    comments = db.relationship('Comment',back_populates = 'author')
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)