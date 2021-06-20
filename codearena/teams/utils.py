import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/team-pictures', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def search_teams(teams=[], tags=[], search_query=""):

    search_query_list = search_query.split()
    team_presubset = []

    team_subset = []
    if tags:
        for team in teams:
            for tag in team.tags.split(','):
                if tag in tags:
                    team_presubset.append(team)
    else:
        team_presubset = teams

    if search_query.strip() == "":
        return team_presubset

    team_presubset_points = [0]*len(team_presubset)

    for i in range(len(team_presubset)):
        team_name = team_presubset[i].name.split()
        for word in team_name:
            for search_word in search_query_list:
                if search_word.lower() in word.lower():
                    team_presubset_points[i] += 1


    while (team_presubset !=[] and max(team_presubset_points) > 0):
        a = team_presubset_points.index(max(team_presubset_points))
        team_subset += [team_presubset[a]]
        team_presubset.pop(a)
        team_presubset_points.pop(a)
        
    return team_subset

