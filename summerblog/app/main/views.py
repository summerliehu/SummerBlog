from flask import render_template, redirect, url_for, flash, abort, request, \
	current_app
from . import main
from ..models import User, Role, Permission, Post
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from flask_login import login_required, current_user
from .. import db
from ..decorators import admin_required
from flask import Markup

@main.route('/', methods=['GET', 'POST'])
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(\
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/about')
def about():
	return render_template('about.html')

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash("Your profile has been updated!")
		return redirect(url_for('main.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile has been updated')
		return redirect(url_for('.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('edit_profile.html', form=form)

@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', posts=[post])

@login_required
@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
	post = Post.query.get_or_404(id)
	user = post.author
	form = PostForm()
	if current_user.is_administrator() and \
	form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, 
			author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.post'))
	form.title.data = post.title
	form.body.data = post.body
	return render_template('edit_post.html', form=form, post=post, user=user)

@login_required
@main.route('/new-post',methods=['GET', 'POST'])
def new_post():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and \
	form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
	return render_template('new_post.html', form=form)


@login_required
@main.route('/delete-post/<int:id>')
def delete_post(id):
	post = Post.query.get_or_404(id)
	#this is a bug, that anyone logged in could delete others post by modifing GET args!!!
	if current_user == post.author or current_user.is_administrator():
		post.delete_post()	
		return redirect(request.args.get('next') or url_for('main.index'))
	else:
		abort(403)

@login_required
@admin_required
@main.route('/blog-admin', methods=['GET', 'POST'])
def blog_admin():
	next=url_for('main.blog_admin')
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('blog_admin.html', **locals())