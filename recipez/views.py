from django.shortcuts import render, redirect
from django.http import HttpResponse
from recipez.forms import UserForm, UserProfileForm, CommentForm
from recipez.models import Recipe, Comment, UserProfile, User


# Home Page
def index(request):
    # recipe_list = Recipe.object.order_by('-creation_time')
    # comment_list = Comment.object.order_by('-creation_time')
    # context_dict = {}
    # context_dict['recipe'] = recipe_list
    # context_dict['comment'] = recipe_list

    return render(request, 'recipez/index.html',
                  # context=context_dict
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


# User Profile Page
def user_profile(request):
    # to be completed

    return render(request, 'recipez/userProfile.html')


# Login Page
def login(request):
    # to be completed

    return render(request, 'recipez/login.html')


# User Registration Form
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

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


# Help Page (About us and Contact us)
def help(request):
    return render(request, 'recipez/help.html')
