from django.shortcuts import render, redirect
from django.http import HttpResponse

from recipez import models
from recipez.forms import UserForm, UserProfileForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipez.models import Recipe, UserProfile, Ingredient, Comment
from django.contrib.auth.models import User


# Home Page
def index(request):
    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        content = request.POST.get('content')
        recipe_list = Recipe.objects.none()
        if search_by == 'user':
            author_list = User.objects.filter(username__icontains=content)
            for author in author_list:
                recipe_list = recipe_list | author.user_profile.recipes.all()

        elif search_by == 'ingredient':
            ingredient_list = Ingredient.objects.filter(name_and_amount__icontains=content)
            for ingredient in ingredient_list:
                recipe_list = recipe_list | ingredient.recipes.all()

        elif search_by == 'name':
            recipe_list = recipe_list | Recipe.objects.filter(name__icontains=content)

        recipe_list = recipe_list.distinct().order_by('-creation_time')
    else:
        recipe_list = Recipe.objects.order_by('-creation_time')
    context_dict = {
        'recipes': recipe_list,
    }

    return render(request,
                  'recipez/index.html',
                  context=context_dict
                  )


# Recipe Detail Page
def show_recipe(request, recipe_name):
    # Data for recipe and existing comments display
    context_dict = {}
    try:
        # Can we find a recipe name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        recipe = Recipe.objects.get(name=recipe_name)  # slug as a index to access to relevant data
        recipe_owner = UserProfile.get(user=recipe.user)
        comments = Comment.objects.filter(recipe=recipe)  # filter to get all data from the comments
        commented_users = UserProfile.objects.filter(username=recipe.user.username)

        context_dict['recipe'] = recipe
        context_dict['recipe_owner'] = recipe_owner
        context_dict['comments'] = comments
        context_dict['commented_users'] = commented_users

    except Recipe.DoesNotExist:
        # We get here if we didn't find the specified recipe.
        # Don't do anything -
        # the template will display the "no recipe" message for us.
        context_dict['recipe'] = None
        context_dict['comments'] = None
        context_dict['commented_users'] = None

     # Form for receiving new comments of current user (request.user.username)
        form = CommentForm()

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                # comment - reference to an instance created
                comment = form.save(commit=True)
            else:
                print(form.errors)
    return render(request, 'recipez/recipe.html',context=context_dict)


# Post a new Recipe
from django import forms
class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ["name","category","region","difficulty","cooking_duration","is_vegan","photo","detail"]


class IngredientModelForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = ["name_and_amount"]

class RecipeAndIngredientForm(forms.Form):
    recipe_form = RecipeModelForm()
    ingredient_form = IngredientModelForm()

def add_recipe(request):

    if request.method == 'POST':
        recipe_form = RecipeModelForm(request.POST, request.FILES)
        ingredient_form = IngredientModelForm(request.POST)
        if recipe_form.is_valid() and ingredient_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user.userprofile
            recipe.save()
            ingredient_name_and_amount = ingredient_form.cleaned_data.get('name_and_amount')
            ingredient = Ingredient.objects.create(name_and_amount=ingredient_name_and_amount)
            ingredient.recipes.add(recipe)
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        recipe_form = RecipeModelForm()
        ingredient_form = IngredientModelForm()
    context = {
        'recipe_form': recipe_form,
        'ingredient_form': ingredient_form,
    }
    return render(request, 'recipez/add_recipe.html',context)


# User Profile Page
def user_profile(request):
    # to be completed

    return render(request, 'recipez/userProfile.html')


# Login Page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('recipez:index'))
            else:
                return HttpResponse("Your Recipez account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'recipez/login.html')


# User Registration Form
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        print(request.POST)
        print(request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'recipez/register.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('recipez:index'))


# Help Page (About us and Contact us)
def help(request):
    return render(request, 'recipez/help.html')
