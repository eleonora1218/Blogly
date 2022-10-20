"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(20),
                            nullable=False)

    last_name = db.Column(db.String(20),
                            nullable=False)

    profile_img = db.Column(db.String(500),
                            nullable=True,
                            default='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')

    
    def __repr__(self):
        """Show user info"""
        u = self
        return f'<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, profile_img={u.profile_img}>'

