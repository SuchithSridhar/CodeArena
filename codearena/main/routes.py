from flask import render_template, request, Blueprint
from codearena.models import User, Team, db
import os

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if not os.path.isfile("./site.db"):
        db.create_all()
    return render_template('index.jinja', title="CodeArena")

@main.route("/about")
def about():
    return render_template('about.jinja', title="About")
