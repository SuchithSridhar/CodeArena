from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from codearena import db, bcrypt
from codearena.models import User, Team
from codearena.teams.forms import NewTeamForm, EditTeamForm, SearchTeamForm
from codearena.teams.utils import save_picture, search_teams

teams = Blueprint('teams', __name__)

@teams.route("/new-team", methods=['get', 'post'])
@login_required
def new_team():
    form = NewTeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data, about=form.about.data, leader=current_user.id)

        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            team.image_file = picture_file

        if form.github.data:
            team.github = form.github.data

        if form.discord.data:
            team.discord = form.discord.data

        if form.tags.data:
            team.tags = form.tags.data

        if form.bio.data:
            team.bio = form.bio.data

        team.members.append(current_user)
        db.session.add(team)
        db.session.commit()
        flash("Team Successfully created!", category="success")
        return redirect(url_for('users.dashboard'))
    return render_template('new-team.jinja', title='New Team', form=form)

@teams.route("/team/<uuid>")
@login_required
def view_team(uuid):
    team = Team.query.get(uuid)
    if not team:
        abort(404, description="Team not found.")

    def get_user_from_id(uuid):
        return User.query.get(uuid)

    return render_template('team-page.jinja', title=team.name, team=team, get_user=get_user_from_id)



@teams.route("/team/join/<uuid>")
@login_required
def join_team(uuid):
    team = Team.query.get(uuid)
    if not team:
        abort(404, description="Team not found.")

    team.members.append(current_user)
    db.session.commit()

    return redirect(url_for('teams.view_team', uuid=uuid))


@teams.route("/team/edit/<uuid>", methods=['get', 'post'])
@login_required
def edit_team(uuid):
    team = Team.query.get(uuid)
    if not team:
        abort(404, description="Team not found.")

    if team.leader != current_user.id:
        abort(403, description="Permission Denied.")

    form = EditTeamForm()
    if request.method == "GET":
        form.name.data = team.name
        form.about.data = team.about
        form.github.data = team.github
        form.discord.data = team.discord
        form.bio.data = team.bio

    if form.validate_on_submit():
        team.name = form.name.data
        team.about = form.about.data
        team.github = form.github.data
        team.discord = form.discord.data
        team.tags = form.tags.data
        team.bio = form.bio.data
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            team.image_file = picture_file

        db.session.commit()
        flash("Team edited successfully!", category="success")
        return redirect(url_for('users.dashboard'))
    return render_template('edit-team.jinja', title='New Team',
            form=form, tags=team.tags.split(',') if team.tags else [])

@teams.route("/search/team", methods=['get', 'post'])
@login_required
def search_team():
    return render_template('search-team.jinja', title='Search Team')

@teams.route('/search/team/api', methods=['post'])
@login_required
def search_api_team():
    search = request.form.get("text")
    tags = request.form.get("tags")
    tags = tags.split(',') if tags.strip()!= "" else []
    teams = Team.query.all()
    teams = search_teams(teams, tags, search)
    result = []
    for team in teams:
        dic = {}
        dic['name'] = team.name
        dic['uuid'] = team.id
        dic['image'] = team.image_file
        dic['about'] = team.about
        dic['tags'] = team.tags

        result.append(dic)
    return jsonify(result)

