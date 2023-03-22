from django import forms
from recipez.models import UserProfile, Comment, Ingredient, Recipe
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CustomFloatInput(forms.widgets.TextInput):
    input_type = 'number'
    template_name = 'django/forms/widgets/number.html'
    step = 'any'
    min_value = 0
    max_value = 5

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'form-control', 'step': self.step, 'min': self.min_value, 'max': self.max_value}
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if value is not None:
            if value < self.min_value or value > self.max_value:
                raise ValidationError(f'Enter a value between {self.min_value} and {self.max_value}.')


class CustomCommentWidget(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control me-2', 'style': 'background: #fff;', 'rows': '4'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class CommentForm(forms.ModelForm):
    detail = forms.CharField(widget=CustomCommentWidget())
    rating = forms.FloatField(widget=CustomFloatInput)

    # Provide additional information
    class Meta:
        # Association between the ModelForm and a model
        model = Comment
        fields = ('rating', 'detail')

class RecipeModelForm(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'region', 'difficulty', 'cooking_duration', 'is_vegan', 'photo', 'detail']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control text-muted', 'placeholder': 'Category'}),
            'region': forms.TextInput(attrs={'class': 'form-control text-muted', 'placeholder': 'Region'}),
            'difficulty': forms.TextInput(attrs={'class': 'form-control text-muted'}),
            'cooking_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'is_vegan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
        }