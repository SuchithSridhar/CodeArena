from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from codearena import db, bcrypt
from codearena.models import User, Team
from codearena.teams.forms import NewTeamForm
from codearena.teams.utils import save_picture

teams = Blueprint('teams', __name__)

@teams.route("/new-team", methods=['get', 'post'])
@login_required
def new_team():
    form = NewTeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, about=form.about.data, team_leader=current_user.id)

        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            team.image_file = picture_file

        if form.github.data:
            team.github = form.github.data

        if form.discord.data:
            team.discord = form.discord.data

        if form.tags.data:
            team.tags = form.tags.data

        db.session.add(team)
        db.session.commit()
        flash("Team Successfully created!")
        return redirect(url_for('users.dashboard'))
    return render_template('new-team.jinja', title='New Team', form=form)
