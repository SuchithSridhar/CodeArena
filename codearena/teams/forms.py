from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from codearena.models import User


class NewTeamForm(FlaskForm):
    name = StringField('Team Name')
    github = StringField('Github Link')
    discord = StringField('Discord Link')
    about = StringField('Team Description')
    bio = TextAreaField('Bio')
    tags = StringField("Tags")
    image_file = FileField('Team Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Team')

class EditTeamForm(FlaskForm):
    name = StringField('Team Name')
    github = StringField('Github Link')
    bio = TextAreaField('Bio')
    discord = StringField('Discord Link')
    about = StringField('Team Description')
    tags = StringField("Tags")
    image_file = FileField('Team Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Team')


class SearchTeamForm(FlaskForm):
    name = StringField('Search')
    tags = StringField("Tags")
    submit = SubmitField('Search')
