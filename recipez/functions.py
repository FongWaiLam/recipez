from recipez.models import Recipe, UserProfile, Ingredient
from django.contrib.auth.models import User
import requests


# search
def search_by(content):
    recipe_list1 = Recipe.objects.none()
    recipe_list2 = Recipe.objects.none()

    author_list = User.objects.filter(username__icontains=content)

    ingredient_list = Ingredient.objects.filter(name_and_amount__icontains=content)
    for ingredient in ingredient_list:
        recipe_list1 = recipe_list1 | ingredient.recipes.all()

    recipe_list2 = recipe_list2 | Recipe.objects.filter(name__icontains=content)

    return {
        'author_list': author_list,
        'recipe_list_by_Ingredient': recipe_list1.distinct().order_by('-creation_time'),
        'recipe_list_by_RecipeName': recipe_list2.order_by('-creation_time')
    }


# get google profile avatar
def update_user_avatar(strategy, *args, **kwargs):
    response = kwargs['response']
    backend = kwargs['backend']
    user = kwargs['user']

    if response['picture']:
        url = response['picture']
        avatar_name = user.username+'.png'
        save_avatar(url, avatar_name)
        new_user_profile = UserProfile.objects.get_or_create(user=user, avatar="/profile_images/"+avatar_name)[0]
        new_user_profile.save()


def save_avatar(image_url, avatar_name):
    img_data = requests.get(image_url).content
    with open('./media/profile_images/'+avatar_name, 'wb') as handler:
        handler.write(img_data)
