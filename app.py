"""Blogly application"""

from flask import Flask, request, render_template,  redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bunniesarebest'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.create_all()


# 127.0.0.1:5000/
@app.route('/')
def homepage():
    """Homepage with list of users & recent posts"""
    user_name = User.query.order_by(User.user_name).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('base.html', user_name=user_name, posts=posts, tags=tags)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

##############################################################################
# USER ROUTES
# USER ROUTES
# USER ROUTES

@app.route('/<int:user_id>')
def details(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/add_user')
def add_user():
    """Form to create new user"""
    return render_template('add_user.html')
@app.route('/add_user', methods=['POST'])
def add_new_user():
    """Create a new user"""
    
    user_name = request.form['user_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_img = request.form['profile_img'] or None

    if user_name == '' or first_name == '' or last_name == '':
        flash ('This is not a valid name')
        return redirect('/add_user')
    else:
        new_user = User(user_name=user_name, first_name=first_name.title(), last_name=last_name.title(), profile_img=profile_img)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>/edit')
def edit_page(user_id):
    """Form to edit user details"""
    user = User.query.get_or_404(user_id)
    return render_template('/edit.html', user=user)
@app.route('/<int:user_id>/edit', methods=['POST'])
def edit_details(user_id):
    """Edit user details"""
    user = User.query.get_or_404(user_id)

    user.user_name = request.form['user_name']
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.profile_img = request.form['profile_img'] or None

    if user.user_name == '' or user.first_name == '' or user.last_name == '':
        flash('This is not a valid name')
        return redirect(f'/{user_id}/edit')
    else:
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

##############################################################################
# POST ROUTES
# POST ROUTES
# POST ROUTES

@app.route('/all_posts')
def all_posts():
    """View all posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('all_posts.html', posts=posts)

@app.route('/post_details/<int:post_id>')
def posts_show(post_id):
    """View individual post. Accessed via homepage"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('post_details.html', post=post, user=user)

@app.route('/<int:user_id>/add_post')
def posts_new_form(user_id):
    """Form to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)
@app.route('/<int:user_id>/add_post', methods=['POST'])
def add_new_post(user_id):
    """Create a post form for a specific user"""

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    if title == '' or content == '':
        flash('Please fill in the title and content.')
        return redirect(f'/{user_id}/add_post')
    else:
        new_post = Post(title=title.capitalize(), content=content.capitalize(), user=user, tags=tags)
        db.session.add(new_post)
        db.session.commit()

    return redirect(f'/{user.id}/user_posts')

@app.route('/post_details/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post from db"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/post_details/<int:post_id>/edit_post')
def edit_post(post_id):
    """Form to edit posts"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, user=user, tags=tags)
@app.route('/post_details/<int:post_id>/edit_post', methods=['POST'])
def submit_edit(post_id):
    """Submits edit to post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    if post.title == '' or post.content == '':
        flash('Please fill in the title and content.')
        return redirect(f'/post_details/{post_id}/edit_post')
    else:
        db.session.add(post)
        db.session.commit()
        return redirect(f'/{user.id}/user_posts')

@app.route('/<int:user_id>/user_posts')
def see_users_posts(user_id):
    """View all posts made by a specific user"""
    user = User.query.get_or_404(user_id)
    post = user.post
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    return render_template('user_posts.html', post=post, user=user, tags=tags)

##############################################################################
# TAG ROUTES
# TAG ROUTES
# TAG ROUTES

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """View an individual tag and see all posts with that tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """Form to create a new tag"""
    posts = Post.query.all()
    return render_template('add_tag.html', posts=posts)
@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Create a new tag"""
    tag_name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    if tag_name == '':
        flash ('This is not a valid tag')
        return redirect('/tags/new')
    else:
        new_tag = Tag(name=request.form['name'], posts=posts)
        db.session.add(new_tag)
        db.session.commit()

    return redirect('/')

@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    # posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag)
@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Submits edit to tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Deletes tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/')





# BUGS TO FIX / FEATURES TO ADD
# BUGS TO FIX / FEATURES TO ADD
# BUGS TO FIX / FEATURES TO ADD

# Auto uppercase first letter: tags.title() tags.capitalize()
