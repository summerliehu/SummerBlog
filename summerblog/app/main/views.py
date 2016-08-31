from flask import render_template, redirect, url_for, flash, abort, request, \
	current_app
from . import main
from ..models import User, Role, Permission, Post, Category, Tag
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, EditCategoryForm, \
	EditTagForm
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
	length = current_app.config['INDEX_BODY_LENGTH']
	return render_template('index.html', posts=posts, pagination=pagination, length=length)

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
		post.title = form.title.data
		post.body=form.body.data
		post.category = Category.query.get(form.category.data)
		db.session.add(post)
		db.session.commit()
		addtags = form.add_tags.data.split()
		for tag in addtags:
			if Tag.query.filter_by(tag_name=tag).first():
				oldtag = Tag.query.filter_by(tag_name=tag).first()
				post.tags.append(oldtag)
				db.session.add(post)
				db.session.commit()
			else:
				newtag = Tag(tag_name=tag)
				db.session.add(newtag)
				db.session.commit()
				post.tags.append(newtag)
				db.session.add(post)
				db.session.commit()
		return redirect(url_for('.post', id=id ))
	form.title.data = post.title
	form.body.data = post.body
	form.category.data = post.category
	return render_template('edit_post.html', form=form, post=post, user=user)

@login_required
@main.route('/new-post',methods=['GET', 'POST'])
def new_post():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and \
	form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object(), \
			category = Category.query.get(form.category.data))
		db.session.add(post)
		db.session.commit()				
		addtags = form.add_tags.data.split()
		for tag in addtags:
			if Tag.query.filter_by(tag_name=tag).first():
				oldtag = Tag.query.filter_by(tag_name=tag).first()
				post.tags.append(oldtag)
				db.session.add(post)
				db.session.commit()
			else:
				newtag = Tag(tag_name=tag)
				db.session.add(newtag)
				db.session.commit()
				post.tags.append(newtag)
				db.session.add(post)
				db.session.commit()		
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
@main.route('/edit-category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
	category = Category.query.get_or_404(id)
	editCategoryForm = EditCategoryForm()
	if current_user.is_administrator() and \
	editCategoryForm.validate_on_submit():
		category.category_name = editCategoryForm.category_name.data
		db.session.add(category)
		return redirect(url_for('main.blog_admin'))
	editCategoryForm.category_name.data = category.category_name
	return render_template('edit_category.html', **locals())

@login_required
@admin_required
@main.route('/delete-category/<int:id>')
def delete_category(id):
	category = Category.query.get_or_404(id)
	if current_user.is_administrator():
		category.delete_category()	
		#return redirect(request.args.get('next') or url_for('main.blog_admin'))
		return redirect(url_for('main.blog_admin'))
	else:
		abort(403)

@login_required
@admin_required
@main.route('/edit-tag/<int:id>', methods=['GET', 'POST'])
def edit_tag(id):
	tag = Tag.query.get_or_404(id)
	form = EditTagForm()
	if current_user.is_administrator() and \
	form.validate_on_submit():
		tag.tag_name = form.tag_name.data
		db.session.add(tag)
		return redirect(url_for('main.blog_admin'))
	form.tag_name.data = tag.tag_name
	return render_template('edit_tag.html', **locals())	

@login_required
@admin_required
@main.route('/delete-tag/<int:id>')
def delete_tag(id):
	tag = Tag.query.get_or_404(id)
	if current_user.is_administrator():
#		for post in tag.posts.all():
#			tag.posts.remove(post)
#		db.session.add(tag)
#		db.session.commit()
#		for post in Post.query.all():
#			post.tags.remove(tag)
#		db.session.add(post)
#		db.session.commit()
#		db.session.delete(tag)
#		db.session.add(tag)
#		db.session.commit()
		all_posts = tag.posts.all()
		for post in all_posts:
			post.tags.delete(tag)
			db.session.add(post)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('main.blog_admin'))
	else:
		abort(403)

@login_required
@admin_required
@main.route('/blog-admin', methods=['GET', 'POST'])
def blog_admin():
	addCategoryForm = EditCategoryForm()
	addTagForm = EditTagForm()
	categories = Category.query.order_by(Category.id.desc()).all()
	tags = Tag.query.order_by(Tag.id.desc()).all()
	page = request.args.get('page', 1, type=int)
	next=url_for('main.blog_admin')
	#posts = Post.query.order_by(Post.timestamp.desc()).all()
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(\
		page, per_page=10, error_out=False)
	posts = pagination.items
	if current_user.is_administrator() and \
	addCategoryForm.validate_on_submit():
		category = Category(category_name=addCategoryForm.category_name.data)
		db.session.add(category)
		return redirect(url_for('.blog_admin'))
	if current_user.is_administrator() and \
	addTagForm.validate_on_submit():
		tag = Tag(tag_name=addTagForm.tag_name.data)
		db.session.add(tag)
		return redirect(url_for('.blog_admin'))
	return render_template('blog_admin.html', **locals())



