from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 128


class UserProfile(models.Model):
    # includes username, password, email
    user = models.OneToOneField(
        User,
        related_name='user_profile',
        on_delete=models.CASCADE
    )

    # List of recipe_id
    bookmark = models.JSONField(null=True, blank=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='profile_images', null=True, blank=True)

    # recipes

    def __str__(self):
        return self.user.username


class Ingredient(models.Model):
    name_and_amount = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name_and_amount


class Recipe(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    name = models.CharField(max_length=MAX_LENGTH)

    # Main dish, Starter, Drink, Dessert...etc
    category = models.CharField(max_length=MAX_LENGTH, default='unknown')

    # Chinese, Japanese, Korean, American, Indian...etc
    region = models.CharField(max_length=MAX_LENGTH, default='unknown')

    # Easy, Medium, Hard...etc
    difficulty = models.CharField(max_length=MAX_LENGTH)

    detail = models.TextField()
    photo = models.ImageField(upload_to='recipe_images', null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    cooking_duration = models.CharField(max_length=MAX_LENGTH)
    is_vegan = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    username = models.CharField(max_length=MAX_LENGTH)

    # 0.0 ~ 5.0
    rating = models.FloatField()

    creation_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    detail = models.TextField()

    def __str__(self):
        return self.detail
