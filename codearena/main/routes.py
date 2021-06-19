from flask import render_template, request, Blueprint
from codearena.models import User

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('layout.html', title="CodeArena")
