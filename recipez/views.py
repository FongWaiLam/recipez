from django.shortcuts import render, redirect
from django.http import HttpResponse
from recipez.forms import UserForm, UserProfileForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipez.models import Recipe, UserProfile, Ingredient, Comment
from django.contrib.auth.models import User
from recipez.functions import search_by


# Home Page
def index(request):
    if request.method == 'POST':
        search_content = request.POST.get('search_content')
        context_dict = search_by(search_content)
    else:
        recipe_list = Recipe.objects.order_by('-creation_time')
        context_dict = {'author_list': None, 'recipe_list_by_Ingredient': None,
                        'recipe_list_by_RecipeName': recipe_list}

    page_list = Recipe.objects.order_by('-likes')[:3]
    context_dict['best_of_today'] = page_list
    return render(request,
                  'recipez/index.html',
                  context=context_dict
                  )


# Recipe Detail Page
def show_recipe(request, recipe_id):
    # Data for recipe and existing comments display
    context_dict = {}
    try:
        # Can we find a recipe.id with the given recipe_id?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        recipe = Recipe.objects.get(id=recipe_id)  # recipe_id as a index to access to relevant data
        comments = Comment.objects.filter(recipe=recipe).order_by(
            '-creation_time')  # filter to get all data from the comments
        all_users = UserProfile.objects.all()

        context_dict['recipe'] = recipe
        context_dict['comments'] = comments
        context_dict['all_users'] = all_users

    except Recipe.DoesNotExist:
        # We get here if we didn't find the specified recipe.
        # Don't do anything -
        # the template will display the "no recipe" message for us.
        context_dict['recipe'] = None
        context_dict['comments'] = None
        context_dict['all_users'] = None

        # Form for receiving new comments of current user (request.user.username)
        form = CommentForm()

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                # comment - reference to an instance created
                comment = form.save(commit=True)
            else:
                print(form.errors)
    return render(request, 'recipez/recipe.html', context=context_dict)


# Post a new Recipe
def add_recipe(request):
    # form = RecipeForm()
    #
    # if request.method == 'POST':
    #     form = RecipeForm(request.POST)
    #
    #     if form.is_valid():
    #         # recipe - reference to an instance created
    #         recipe = form.save(commit=True)
    #         print(recipe, recipe.slug)
    #         return redirect('/rango/')
    #     else:
    #         print(form.errors)

    return render(request, 'recipez/add_recipe.html',
                  # {'form': form}
                  )


# Post a new Comment
def add_comment(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.username = request.user.username
            comment.save()

    return render(request, 'recipez/add_comment.html', {'form': form})

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
