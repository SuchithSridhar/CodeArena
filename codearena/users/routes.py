import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from codearena import db, bcrypt
from codearena.models import User, Team
from codearena.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from codearena.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['get', 'post'])
def register():
    if not os.path.isfile("./site.db"):
        db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.jinja', title='Register', form=form)

@users.route("/login", methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        form.email.data = form.email.data.lower()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.jinja', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account")
@login_required
def account():
    return render_template('account.jinja', title='Account',
            skills=current_user.skills.split(',') if current_user.skills else [])

@users.route("/account/edit", methods=['get', 'post'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.github.data:
            current_user.github = form.github.data
        if form.personal.data:
            current_user.personal_site = form.personal.data
        if form.linkedin.data:
            current_user.linkedin = form.linkedin.data
        if form.skills.data:
            current_user.skills = form.skills.data
        if form.bio.data:
            current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.github.data = current_user.github
        form.bio.data = current_user.bio
        form.linkedin.data = current_user.linkedin
        form.personal.data = current_user.personal_site
    return render_template('edit-account.jinja', title='Edit Account',
            form=form, skills=current_user.skills.split(',') if current_user.skills else [])


@users.route("/dashboard")
@login_required
def dashboard():
    # team = Team(name="We Code", about="A group of programmers who love to code just doing there work.", leader_id=current_user.id )
    # db.session.add(team)
    # db.session.commit()
    return render_template('dashboard.jinja', title="Dashboard", teams=Team.query.all())
