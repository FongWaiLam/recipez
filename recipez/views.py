from django.shortcuts import render, redirect
from django.http import HttpResponse


# Home Page
def index(request):
    # recipe_list = Recipe.object.order_by('-creation_time')
    # comment_list = Comment.object.order_by('-creation_time')
    # context_dict = {}
    # context_dict['recipe'] = recipe_list
    # context_dict['comment'] = recipe_list

    return render(request, 'recipez/index.html', context=context_dict)

# Recipe Detail Page
def show_recipe(request):

    # # Data for recipe and existing comments display
    # context_dict = {}
    # try:
    #     # Can we find a recipe name slug with the given name?
    #     # If we can't, the .get() method raises a DoesNotExist exception.
    #     # The .get() method returns one model instance or raises an exception.
    #     recipe = Recipe.objects.get(slug=recipe_id_slug)  # slug as a index to access to relevant data
    #     comments = Comment.objects.filter(recipe=recipe)  # filter to get all data from the comments
    #     commented_users = User.objects.filter(comments.username=username)
    #
    #     context_dict['recipe'] = recipe
    #     context_dict['comments'] = comments
    #     context_dict['User'] = commented_users
    #
    # except Recipe.DoesNotExist:
    #     # We get here if we didn't find the specified recipe.
    #     # Don't do anything -
    #     # the template will display the "no recipe" message for us.
    #     context_dict['recipe'] = None
    #     context_dict['comments'] = None
    #
    #  # Form for receiving new comments of current user (request.user.username)
    #     form = RecipeForm()
    #
    #     if request.method == 'POST':
    #         form = RecipeForm(request.POST)
    #
    #         if form.is_valid():
    #             # recipe - reference to an instance created
    #             recipe = form.save(commit=True)
    #             print(recipe, recipe.slug)
    #             return redirect('/rango/')
    #         else:
    #             print(form.errors)

        # Go render the response and return it to the client.
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

    return render(request, 'rango/add_recipe.html', {'form': form})

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

    return render(request, 'recipez/register.html')

# Help Page (About us and Contact us)
def help(request):
    return render(request, 'recipez/help.html')
