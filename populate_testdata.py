import os
import yaml
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recipez_project.settings')

import django
django.setup()

from recipez.models import UserProfile, Recipe, Ingredient, Comment
from django.contrib.auth.models import User


def load_db_data(yaml_path):
    with open(yaml_path, 'r') as stream:
        try:
            print("Loading yaml file...")
            db_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"An Exception occurred while loading yaml file!\n {exc}")
    return db_data

def populate():
    path = os.path.dirname(os.path.abspath(__file__)) # Path to current directory
    avatar_name_path = os.path.join(path, 'media/profile_images')
    avatar_name_list = os.listdir(avatar_name_path)
    db_yaml_path = os.path.join(path, 'db_data.yml') # Path to yaml file
    db_data = load_db_data(yaml_path=db_yaml_path)

    print(db_data)

    counter = 0
    for i in db_data['users']:
        print(f"Adding user: {i['username']}")
        a = add_user(i['username'], i['password'], i['mail'])
        add_user_profile(a, avatar_name_list[counter])
        counter +=1
        
        # Add recipes and details from the db_data.yml file
        recipes = i['recipes']
        if recipes is not None:
            for recipe in recipes:
                print(f"Adding recipe: {recipe['name']}")
                ingredients = add_ingredients(ingredients=recipe['ingredients']) # Takes the ingredients object from the db and passes to recipes below
                add_recipe(User.objects.get(username=i['username']).user_profile, recipe['name'], recipe['category'],
                           recipe['detail'], recipe['region'], ingredients, recipe['photo_name'], recipe['cooking_duration'],
                           recipe['difficulty'], recipe['vegan'], recipe['likes'])

    # Add comments to recipes
    for i in db_data['comments']:
        print(f"Adding comment to recipe: {i['name']}")
        add_comment(
            recipe=Recipe.objects.filter(name=i['name']).first(), 
            username=i['username'], 
            rating=i['rating'], detail=i['comment']
            )

    # Add bookmarks to recipes
    recipe_id_list = []
    recipe_list = Recipe.objects.all()
    for recipe in recipe_list:
        print(f"Adding bookmark to recipe: {recipe.name}")

        recipe_id = random.randint(0, 14)
        tester_id = random.randint(1, 9)

        recipe_id_list.append(recipe.id)
        add_bookmark(User.objects.get(id=tester_id), recipe_id_list)


def add_user(username, password, email):
    a = User.objects.get_or_create(username=username)[0]
    a.set_password(password)
    a.email = email
    a.save()
    return a


def add_user_profile(user, avatar_name):
    b = UserProfile.objects.get_or_create(user=user)[0]
    b.avatar = "/profile_images/" + avatar_name
    b.save()


def add_ingredients(ingredients):
    c = Ingredient.objects.get_or_create(name_and_amount=ingredients)[0]
    c.save()
    return c # Returns the ingredient object from the database that's been created


def add_recipe(user_profile, name, category, detail, region, ingredients, photo_name, cooking_duration, difficulty, vegan, likes):
    d = Recipe.objects.get_or_create(user=user_profile, name=name, category=category, detail=detail, region=region,
                                     photo="/recipe_images/" + photo_name, cooking_duration=cooking_duration,
                                     difficulty=difficulty, is_vegan=vegan, likes=likes)[0]
    d.ingredients.add(ingredients) # Builds relation between recipe and ingredients

    sum_, size = 0, 0
    for k in d.comments.all():
        sum_ += k.rating
        size += 1
    if size == 0:
        d.average_rating = 0
    else:
        d.average_rating = sum_ / size

    d.save()


def add_comment(recipe, username, rating, detail):
    e = Comment.objects.get_or_create(recipe=recipe, username=username, rating=rating, detail=detail)[0]
    e.save()


def add_bookmark(user, recipe_id_list):
    f = UserProfile.objects.get(user=user)
    f.bookmark = recipe_id_list
    f.save()


if __name__ == '__main__':
    populate()
    print("Finished...")
