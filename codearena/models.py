from uuid import uuid4
from datetime import datetime
from flask import current_app
from codearena import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

def create_uuid():
    return str(uuid4())


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=create_uuid)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.email}', '{self.image_file}')"

