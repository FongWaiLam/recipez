from django import forms
from recipez.models import UserProfile, Comment, Ingredient, Recipe
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)

class CommentForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea)
    # Provide additional information
    class Meta:
        # Association between the ModelForm and a model
        model = Comment
        fields = ('detail',)

from django import forms
class RecipeModelForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Recipe
        fields = ["name","category","region","difficulty","cooking_duration","is_vegan","photo","detail"]
# class IngredientModelForm(forms.ModelForm):
#     class Meta:
#         model = Ingredient
#         fields = ["name_and_amount"]

