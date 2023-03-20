from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class ShowRecipeViewTests(TestCase):
    def test_show_recipe_view_with_no_recipe(self):

        response = self.client.get(reverse('recipez:show_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')
        self.assertQuerysetEqual(response.context['recipe'], None)
