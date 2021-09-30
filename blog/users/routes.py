from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from blog import bcrypt, db
from blog.models import User, Post
from blog.users.utils import save_picture, send_reset_email
from blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__)

@users.route("/register", methods=['Get', 'Post'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {form.username.data}! Please log in', category='success')
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['Get', 'Post'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user and bcrypt.check_password_hash(exist_user.password, form.password.data):
            login_user(exist_user, remember=form.remember.data)
            next_page = request.args.get('next') # args is dict. we can args['next'], but this will throw an error whenever they cannot find next. So get will throw None, which is better.
            if next_page:
                next_page = next_page.split('/')
            flash(f'Logged in as {form.email.data}!', category='success')
            return redirect(f'{next_page[-1]}_page') if next_page else redirect(url_for('main.home_page'))
        else:
            flash('Login Unsuccessful! Please check email and password', category='danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('main.home_page'))


@users.route("/account", methods=['Get', 'Post'])
@login_required
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash('Account information updated!', category='success')
        return redirect(url_for('users.account_page'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+str(current_user.image_file))
    return render_template('account.html', title='Account', image_file=image_file,form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page_number = request.args.get('page',1,type=int) # 1 is the default value
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post\
        .query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page_number)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route('/reset_password', methods=['Get', 'Post'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent with instructions to reset your password', category='info')
        return redirect(url_for('users.login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['Get', 'Post'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'That is an invalid or expired token.', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = password_hash
        db.session.commit()
        flash(f'Your password has been updated! Please log in', category='success')
        return redirect(url_for('users.login_page'))
    return render_template('reset_token.html', title="Reset Password", form=form)