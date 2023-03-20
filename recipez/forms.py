from django import forms
from django.core.exceptions import ValidationError

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
    username = forms.CharField(widget=forms.HiddenInput())
    is_active = forms.BooleanField(widget=forms.HiddenInput())

    detail = forms.CharField(widget=CustomCommentWidget())
    rating = forms.FloatField(widget=CustomFloatInput)

    # Provide additional information
    class Meta:
        # Association between the ModelForm and a model
        model = Comment
        exclude = ('recipe', 'creation_time')
