import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile-pictures', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def search_users(people, tags, search_query=""):

        search_query_list = search_query.split()
        people_presubset = []

        people_subset = []
        if tags:
            for ppl in people:
                for tag in ppl.skills.split(','):
                    if tag in tags:
                        people_presubset.append(ppl)
        else:
            people_presubset = people

        if search_query.strip() == "":
            return people_presubset

        print(people, tags, search_query)
        people_presubset_points = [0]*len(people_presubset)

        for i in range(len(people_presubset)):
            people_name = people_presubset[i].username.split()
            for word in people_name:
                for search_word in search_query_list:
                    if search_word.lower() in word.lower():
                        people_presubset_points[i] += 1


        while (people_presubset !=[] and max(people_presubset_points) > 0):
            a = people_presubset_points.index(max(people_presubset_points))
            people_subset += [people_presubset[a]]
            people_presubset.pop(a)
            people_presubset_points.pop(a)
            
        return people_subset 
