from . import db
from flask_login  import UserMixin
from datetime import datetime,date
from sqlalchemy import func
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app



class Base:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def commit(self):
        db.session.commit()

class User(db.Model,Base,UserMixin):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    fullname=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    about=db.Column(db.Text,nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    profile_image=db.Column(db.String(100),nullable=False,default='default_profile_pic.png')
    join_date=db.Column(db.Date,nullable=False, default=date.today)
    password=db.Column(db.String(2000),nullable=False)

    posts=db.relationship('Post',backref='users', lazy=True,cascade="all, delete-orphan")
    subscribers=db.relationship('Subscriber',backref='users', lazy=True,cascade="all, delete-orphan")
    comments=db.relationship('Comment',backref='user_comments',lazy=True,cascade="all, delete-orphan")

    def get_reset_token(self, expires_sec=1800):
        token_serializer= Serializer(current_app.config['SECRET_KEY'])
        return token_serializer.dumps(self.email, salt='password-reset')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        token_serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = token_serializer.loads(token, salt='password-reset', max_age=expires_sec)
        except:
            return None
        return User.query.filter_by(email=email).first()


    def __repr__(self):
        return f"User(id={self.id}, name='{self.username}', name='{self.fullname}', email='{self.email}')"


class Post(db.Model,Base):
    __tablename__='posts'

    id=db.Column(db.Integer,primary_key=True)
    heading=db.Column(db.String(150),nullable=False)
    content=db.Column(db.Text,nullable=False)
    date_posted=db.Column(db.Date, nullable=False,default=date.today)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    likes=db.Column(db.Integer,default=0,nullable=False)
    comment_count=db.Column(db.Integer,default=0,nullable=False)

    comments=db.relationship('Comment',backref='post_comments',lazy=True,cascade="all, delete-orphan")

class Comment(db.Model,Base):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),nullable=False)
    feedback=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.Date, nullable=False,default=date.today)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)

class Subscriber(db.Model,Base):
    __tablename__='subscribers'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)


    
