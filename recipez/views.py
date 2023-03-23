# Import modules and functions
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from recipez.forms import UserForm, UserProfileForm, CommentForm, RecipeModelForm
from recipez.functions import search_by, is_ajax
from recipez.models import Recipe, UserProfile, Ingredient, Comment


# Create your views here.

# Home Page
def index(
    request, template='recipez/index/index.html', extra_context=None):
    if request.method == 'POST':
        search_content = request.POST.get('search_content')
        context_dict = search_by(search_content)
        return render(request, 'recipez/search.html', context=context_dict)
    RECIPE_PER_PAGE = 3
    page = int(request.GET.get('page', 1))

    # Enable Pagination for the recipe list
    recipe_list = Recipe.objects.all().order_by('-creation_time')
    p = paginator.Paginator(recipe_list, RECIPE_PER_PAGE)
    try:
        recipe_page = p.page(page)
    except paginator.EmptyPage:
        recipe_page = paginator.Page([], page, p)

    if not is_ajax(request):
        context_dict = {'author_list': None, 'recipe_list_by_Ingredient': None,
                        'recipe_list_by_RecipeName': recipe_page}
        best_pages = Recipe.objects.order_by('-likes')[:3]
        context_dict['best_of_today'] = best_pages
        return render(request,
                      'recipez/index/index.html',
                      context=context_dict
                      )

    elif is_ajax(request):
        content = ''
        page = int(request.GET.get('page'))
        try:
            recipe_page = p.page(page)
        except paginator.EmptyPage:
            recipe_page = paginator.Page([], page, p)

        for post in recipe_page:
            content += render_to_string('recipez/index/index_post_item.html',
                                        {'recipe': post},
                                        request=request)
        return JsonResponse({
            "content": content,
            "end_pagination": True if page >= p.num_pages else False,
        })


# Recipe Detail Page
def show_recipe(request, recipe_id):
    context_dict = {}
    # Form for receiving new comments of current user (request.user.username)
    form = CommentForm()
    context_dict['form'] = form

    try:
        recipe = Recipe.objects.get(id=recipe_id)  # recipe_id as a index to access to relevant data
        comments = Comment.objects.filter(recipe=recipe).order_by(
            '-creation_time')  # filter to get all data from the comments
        all_users = UserProfile.objects.all()

        context_dict['recipe'] = recipe
        context_dict['comments'] = comments
        context_dict['all_users'] = all_users

        # check likes and bookmarks
        context_dict['is_liked'] = 'Like'
        context_dict['is_bookmark'] = 'Add to bookmark'
        if request.user.is_authenticated:
            u_profile = request.user.user_profile
            is_liked = u_profile.liked_recipes.filter(id=recipe_id)
            if is_liked.exists():
                context_dict['is_liked'] = 'Liked'
            if request.user.user_profile.bookmark is None:
                u_profile.bookmark = []
                u_profile.save()
            else:
                if int(recipe_id) in request.user.user_profile.bookmark:
                    context_dict['is_bookmark'] = 'Already in bookmark'

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.username = request.user.username
                comment.save()

    except Recipe.DoesNotExist:
        # We get here if we didn't find the specified recipe.
        context_dict['recipe'] = None
        context_dict['comments'] = None
        context_dict['all_users'] = None

    return render(request, 'recipez/recipe.html', context=context_dict)


# Post a new Recipe
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeModelForm(request.POST)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user.user_profile
            if 'photo' in request.FILES:
                recipe.photo = request.FILES['photo']
            recipe.save()
            print("recipe saved")
            sum_ingredients = int(request.POST.get('ingredient_set-TOTAL_FORMS'))
            for i in range(0, sum_ingredients):
                ingredient_name = request.POST.get('ingredient_set-' + str(i) + '-ingredient')
                print(ingredient_name)
                ingredient = Ingredient.objects.get_or_create(name_and_amount=ingredient_name)[0]
                print(ingredient)
                ingredient.recipes.add(recipe)
                ingredient.save()
            print("ingredient saved")
            messages.success(request, "You have successfully added a new recipe!")
            return redirect(reverse('recipez:index'))

    else:
        recipe_form = RecipeModelForm()
    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'recipez/add_recipe.html', context)


# User Profile Page
def user_profile(request, user_name):
    user = User.objects.get(username=user_name)
    # userProfile = user.user_profile

    avatar = user.user_profile.avatar  # Get the user's avatar

    post_recipes = user.user_profile.recipes.all()  # Get the user's all posted recipes
    saved_recipes_id = user.user_profile.bookmark  # Get the user's saved recipes (list of recipe_id)

    saved_recipes = []
    if saved_recipes_id:
        for item_id in saved_recipes_id:
            saved_recipes.append(Recipe.objects.get(id = item_id))
    
    context_dict = {
        'user_name': user_name,
        'user_avatar': avatar,
        'post_recipes': post_recipes,
        'saved_recipes': saved_recipes
    }

    return render(request, 'recipez/user_profile.html', context=context_dict)


# Login Page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('usernameInput')
        password = request.POST.get('passwordInput')
        remember_me = request.POST.get('rememberMe')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # set session expire time to 0
                messages.success(request, "You have been successfully logged in!")
                return redirect(reverse('recipez:index'))
            else:
                return HttpResponse("Your Recipez account is disabled.")
        else:
            # print(f"Invalid login details: {username}, {password}") # Not required, only for debugging
            messages.error(request, f"Your login details are incorrect, {username}")
            return redirect(reverse('recipez:login'))

    else:
        return render(request, 'recipez/authentication/login.html')


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

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

        if registered:
            messages.success(request, "You have been successfully registered! Please log in.")
            return redirect(reverse('recipez:login'))
        else:
            messages.error(request, "Please check your registration details.")
            return redirect(reverse('recipez:register'))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'recipez/authentication/register.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect(reverse('recipez:index'))


@login_required
def like_recipe(request, recipe_id):
    u_profile = request.user.user_profile
    target_recipe = Recipe.objects.get(id=recipe_id)
    is_liked = request.user.user_profile.liked_recipes.filter(id=recipe_id)

    if is_liked.exists():
        u_profile.liked_recipes.remove(target_recipe)
        target_recipe.likes -= 1
    else:
        u_profile.liked_recipes.add(target_recipe)
        target_recipe.likes += 1

    u_profile.save()
    target_recipe.save()

    return redirect(reverse('recipez:show_recipe', kwargs={'recipe_id': recipe_id}))


@login_required
def add_bookmark(request, recipe_id):
    u_profile = request.user.user_profile

    if int(recipe_id) in u_profile.bookmark:
        u_profile.bookmark.remove(int(recipe_id))
    else:
        u_profile.bookmark.append(int(recipe_id))

    u_profile.save()

    return redirect(reverse('recipez:show_recipe', kwargs={'recipe_id': recipe_id}))


# About Page (About us and Contact us)
def about(request):
    return render(request, 'recipez/about.html')
