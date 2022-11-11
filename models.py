"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time, Interval
db = SQLAlchemy()

def connect_db(app):
    """Connects db to provided Flask app"""
    db.app=app
    db.init_app(app)


class User(db.Model):
    """Blog users who may have many posts"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    user_name = db.Column(db.String(20),
                            nullable=False,
                            unique=True)

    first_name = db.Column(db.String(20),
                            nullable=False)

    last_name = db.Column(db.String(20),
                            nullable=False)

    profile_img = db.Column(db.String(500),
                            nullable=True,
                            default='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')

    post = db.relationship('Post', backref='User', cascade="all, delete-orphan")

    def __repr__(self):
        """Show user info in nice format"""
        u = self
        return f'<User id={u.id}, user_name={u.user_name}, first_name={u.first_name}, last_name={u.last_name}, profile_img={u.profile_img}>'


class Post(db.Model):
    """Posts on a blog by users"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    unique=True)

    post_user = db.Column(db.Text, 
                            db.ForeignKey('users.user_name'))

    title = db.Column(db.Text,
                        nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.now)

    user = db.relationship('User', backref='Post', cascade="all,delete")

    def __repr__(self):
        """Show post info"""
        p = self
        return f'<Post {p.id} {p.post_user} {p.title} {p.content} {p.created_at} >'

    @property
    def display_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

