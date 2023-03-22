from django.test import TestCase
from django.urls import reverse
from recipez.models import Recipe, User, Ingredient, UserProfile


# Create your tests here.

# class ShowRecipeViewTests(TestCase):
#     def test_show_recipe_view_with_no_recipe(self):

#         response = self.client.get(reverse('recipez:show_recipe'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, '')
#         self.assertQuerysetEqual(response.context['recipe'], None)

# Testing Database
class UserProfileTest(TestCase):
    def setUp(self):
        User.objects.create(username="MyTester1", email="mytester1@gmail.com", password="password")

    def test_return_user(self):
        """If User is correct, check for username"""
        user = User.objects.get(username="MyTester1")
        self.assertEqual(user.username, 'MyTester1')
    def test_return_mail(self):
        """If User is correct, check for email"""
        user = User.objects.get(email="mytester1@gmail.com")
        self.assertEqual(user.email, 'mytester1@gmail.com')
    def test_return_password(self):
        """If User is correct, check for password"""
        user = User.objects.get(password="password")
        self.assertEqual(user.password, 'password')

class RecipeTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username="MyTester1", email="mytester1@gmail.com", password="password")
        test_user_profile = UserProfile.objects.create(user=test_user)
        test_r1 = Recipe.objects.create(user=test_user_profile,name="test_recipe", category="main", region="chinese", 
                                    difficulty="easy", detail="test_detail", cooking_duration="test_duration")
        test_r1.ingredients.add(Ingredient.objects.create(name_and_amount="test_ingredient"))
    
    def test_recipe_creation(self):
        """If Recipe is created, check for name, category, region, difficulty, detail, cooking_duration, ingredients"""
        recipe = Recipe.objects.get(name="test_recipe")
        self.assertEqual(recipe.name, 'test_recipe')
        self.assertEqual(recipe.category, 'main')
        self.assertEqual(recipe.region, 'chinese')
        self.assertEqual(recipe.difficulty, 'easy')
        self.assertEqual(recipe.detail, 'test_detail')
        self.assertEqual(recipe.cooking_duration, 'test_duration')
    
    def test_recipe_ingredient(self):
        """If Recipe is created, check for ingredients"""
        recipe = Recipe.objects.get(name="test_recipe")
        ingredient = Ingredient.objects.get(name_and_amount="test_ingredient")
        self.assertEqual(recipe.ingredients.get(), ingredient)

# Testing Views
class IndexViewTests(TestCase):
    def test_index_view_with_no_recipe(self):
        response = self.client.get(reverse('recipez:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('recipe'), None)

    def test_index_view_with_a_recipe(self):
        test_user = User.objects.create(username="MyTester1", email="tester1@gmail.com", password="password")
        test_user_profile = UserProfile.objects.create(user=test_user)
        test_r1 = Recipe.objects.create(user=test_user_profile,name="test_recipe", category="main", region="chinese",
                                    difficulty="easy", detail="test_detail", cooking_duration="test_duration")
        test_r1.ingredients.add(Ingredient.objects.create(name_and_amount="test_ingredient"))
        response = self.client.get(reverse('recipez:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_recipe")
        self.assertEqual(response.context['recipe'], Recipe.objects.get(name="test_recipe"))

class ShowRecipeViewTests(TestCase):
    def test_show_recipe_view_with_no_recipe(self):
        response = self.client.get(reverse('recipez:show_recipe', kwargs={'recipe_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('recipe'), None)

    def test_show_recipe_view_with_a_recipe(self):
        test_user = User.objects.create(username="MyTester1", email="tester1@gmail.com", password="password")
        test_user_profile = UserProfile.objects.create(user=test_user)
        test_r1 = Recipe.objects.create(user=test_user_profile,name="test_recipe", category="main", region="chinese",
                                    difficulty="easy", detail="test_detail", cooking_duration="test_duration")
        test_r1.ingredients.add(Ingredient.objects.create(name_and_amount="test_ingredient"))
        response = self.client.get(reverse('recipez:show_recipe', kwargs={'recipe_id': test_r1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_recipe")
        self.assertEqual(response.context['recipe'], Recipe.objects.get(name="test_recipe"))

class AddRecipeViewTests(TestCase):
    def test_add_recipe_view_with_no_recipe(self):
        response = self.client.get(reverse('recipez:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('recipe'), None)

    def test_add_recipe_view_with_a_recipe(self):
        test_user = User.objects.create(username="MyTester1", email="tester1@gmail.com", password="password")
        test_user_profile = UserProfile.objects.create(user=test_user)
        test_r1 = Recipe.objects.create(user=test_user_profile,name="test_recipe", category="main", region="chinese",
                                    difficulty="easy", detail="test_detail", cooking_duration="test_duration")
        test_r1.ingredients.add(Ingredient.objects.create(name_and_amount="test_ingredient"))
        response = self.client.get(reverse('recipez:add_recipe'))
        self.assertEqual(response.status_code, 200)
