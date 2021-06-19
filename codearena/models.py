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

team_user = db.Table('team_members',
    db.Column('team_id', db.String, db.ForeignKey('team.id'), nullable=False),
    db.Column('user_id', db.String, db.ForeignKey('user.id'), nullable=False)
)    

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=create_uuid)
    username = db.Column(db.String(20), unique=True, nullable=False)
    user_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bio =  db.Column(db.Text, nullable=True)
    github = db.Column(db.String(120), unique=False, nullable=True)
    linkedin = db.Column(db.String(120), unique=False, nullable=True)
    personal_site = db.Column(db.String(120), unique=False, nullable=True)
    # team_invitations
    # socail_network = db.column(db.Text)
    skills =  db.Column(db.Text, nullable=True)
    

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.email}', '{self.image_file}')"

class Team(db.Model):
    id = db.Column(db.String, primary_key=True, default=create_uuid)
    name = db.Column(db.String(20), unique=False, nullable=False)
    about = db.Column(db.Text)
    # join_request = //check here
    date_crated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    github = db.Column(db.String(120), unique=False, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    leader_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    team_members = db.relationship('User', secondary=team_user, lazy=True,
        backref=db.backref('team_members', lazy='dynamic'))

    def __repr__(self):
        return f"Team('{self.id}, {self.name}', '{self.about}', '{self.image_file}')"

