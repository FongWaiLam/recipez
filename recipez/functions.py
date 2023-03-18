from django.shortcuts import render, redirect
from django.http import HttpResponse
from recipez.forms import UserForm, UserProfileForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipez.models import Recipe, UserProfile, Ingredient, Comment
from django.contrib.auth.models import User


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
