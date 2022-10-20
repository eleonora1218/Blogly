"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bunniesarebest'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# flask refuses to run with db.create_all()
app.app_context().push()

connect_db(app)
db.create_all()

# 127.0.0.1:5000/
@app.route('/')
def homepage():
    """Homepage with list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('base.html', users=users)

@app.route('/add_user')
def add_user():
    """Form to add a new user"""
    return render_template('add_user.html')

@app.route('/', methods=['POST'])
def add_new_user():
    """Create user page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_img = request.form['profile_img'] or None

    if first_name == '' or last_name == '':
        flash ('This is not a valid name')
        return redirect('/add_user')
    else:
        new_user = User(first_name=first_name, last_name=last_name, profile_img=profile_img)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>')
def details(user_id):
    """View user's details"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/<int:user_id>/edit')
def edit_page(user_id):
    """Sends user to route to edit details"""
    user = User.query.get_or_404(user_id)
    return render_template('/edit.html', user=user)

@app.route('/<int:user_id>/edit', methods=['POST'])
def edit_details(user_id):
    """Allows user to edit their name & profile picture"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.profile_img = request.form['profile_img'] or None

    db.session.add(user)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404