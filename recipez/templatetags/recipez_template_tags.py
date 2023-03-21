from django import template
from recipez.models import UserProfile
from django.contrib.auth.models import User

register = template.Library()


# this is a decorator, that will take the return value of the get_category_list() method
# and then proceed in the back end.
# assign the html to be merged to the using page

# when method called in html tag, it will retutn the html merged the following things

@register.inclusion_tag('recipez/includes/base.html')
def get_user_avatar_url(request):
    # The current user_profile will be passed to the base.html
    # then the html merge with the following return value will pass to the html called this tag.
    return {'user_avatar': UserProfile.objects.filter(user=request.user).avatar.url}
