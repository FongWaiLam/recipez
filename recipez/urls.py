from django.urls import path
from recipez import views

app_name = 'recipez'
urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<recipe_id>/', views.show_recipe, name='show_recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('user_profile/<user_name>/', views.user_profile, name='user_profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('help/', views.help, name='help'),
    path('logout/', views.user_logout, name='logout'),
    path('like/<recipe_id>/', views.like_recipe, name='like_recipe'),
    path('add_bookmark/<recipe_id>/', views.add_bookmark, name='add_bookmark'),
]