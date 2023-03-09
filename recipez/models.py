from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 128


class UserProfile(models.Model):
    # includes username, password, email
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bookmark = models.JSONField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    # recipes

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    name = models.CharField(max_length=MAX_LENGTH)
    category = models.CharField(max_length=MAX_LENGTH)
    detail = models.TextField()
    region = models.CharField(max_length=MAX_LENGTH)
    photo = models.ImageField(upload_to='recipe_images', blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    cooking_duration = models.CharField(max_length=MAX_LENGTH)
    difficulty = models.CharField(max_length=MAX_LENGTH)
    is_vegan = models.BooleanField(default=False)
    # ingredients
    # comments

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipes = models.ManyToManyField(
        Recipe,
        related_name='ingredients'
    )

    name = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    username = models.CharField(max_length=MAX_LENGTH)
    rating = models.FloatField()
    creation_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    detail = models.TextField()

    def __str__(self):
        return self.detail
