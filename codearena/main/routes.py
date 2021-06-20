from flask import render_template, Blueprint, redirect
from flask_login import current_user
from flask.helpers import url_for
from codearena.models import User, Team, db
import os

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    return render_template('index.jinja', title="CodeArena")

@main.route("/about")
def about():
    return render_template('about.jinja', title="About")
