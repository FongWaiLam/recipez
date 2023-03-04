from django.urls import path
from recipez import views

app_name = 'recipez'
urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/,slug:recipe_id_slug>/', views.show_recipe, name='show_recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('help/', views.help, name='help'),
]