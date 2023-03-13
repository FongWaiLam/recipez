from django import forms
from recipez.models import UserProfile, Comment
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