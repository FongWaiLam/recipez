import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recipez_project.settings')

import django
django.setup()

from recipez.models import UserProfile, Recipe, Ingredient, Comment
from django.contrib.auth.models import User


ingredient_list1 = ['150g wholegrain rice', '50ml soy sauce', '2 tbsp mirin', '0.5 tsp grated ginger',
                    '1 tsp honey', '350g firm tofu (we used Cauldron)', '1 bunch spring onions, ends trimmed',
                    '2 tsp sunflower oil', '0.5 tsp sesame seeds', '1 red chilli, sliced (optional)']

ingredient_list2 = ['4 tbsp olive oil', '1 onion, finely chopped', '2 garlic cloves, crushed',
                    '0.25 tsp chilli flakes', '2 x 400g cans chopped tomatoes', '1 tsp caster sugar',
                    '6 tbsp mascarpone', '4 skinless chicken breasts, sliced into strips', '300g penne',
                    '70g mature cheddar, grated', '50g grated mozzarella',
                    '0.5 small bunch of parsley, finely chopped']

ingredient_list3 = ['1 tbsp rapeseed oil', '1 onion, finely chopped', '2 carrots, finely diced',
                    '2 celery sticks, finely diced', '2 garlic cloves, thinly sliced', '500g carton tomato passata',
                    '2 tbsp chopped parsley', '400g lean mince turkey', '4 tbsp porridge oats', 'pinch paprika',
                    '1 garlic clove, crushed', 'spray of oil']

ingredient_list4 = ['150g unsalted butter, plus extra for the ramekins',
                    '200g dark chocolate (70% cocoa), roughly chopped', '90g golden caster sugar', '3 large eggs',
                    '90ml Guinness', 'clotted cream or thick double cream, to serve (optional)']

ingredient_list5 = ['500g potatoes, peeled and chopped', '2 x 400g cans cannellini beans, drained',
                    '3 tbsp chopped fresh coriander', '1 tsp chilli powder', '2 tsp olive oil',
                    '2 tbsp finely chopped ginger', '1 red chilli, deseeded for less spice', '2 tbsp cumin seeds',
                    '2 tbsp ground coriander', '1 tsp chilli powder', '400g leeks, thickly sliced',
                    '1 red pepper, deseeded and diced', '1 green pepper, deseeded and diced',
                    '2 large skinless chicken breasts, about 400g, diced', '400g can chopped tomatoes',
                    '2 tbsp tomato purée', '2 tsp vegetable bouillon',
                    '3 tbsp peanut butter (with no sugar or palm oil)', '320g broccoli, to serve']

ingredient_list6 = ['1 tbsp rapeseed oil, plus a drizzle to serve (optional)', '2 large garlic cloves, chopped',
                    '500g leeks, thinly sliced', '500g potatoes, cut into cubes',
                    '500ml vegan vegetable stock, made with 1.5 tsp bouillon powder',
                    '500ml unsweetened almond milk', 'chopped chives and bread, to serve']


def populate():
    avatar_name_list = os.listdir("./media/profile_images")
    for i in range(0, 10):
        name = 'tester' + str(i)
        a = add_user(name, name + '123', name + '@gmail.com')
        add_user_profile(a, avatar_name_list[i])

    add_ingredients(ingredient_list1)
    add_ingredients(ingredient_list2)
    add_ingredients(ingredient_list3)
    add_ingredients(ingredient_list4)
    add_ingredients(ingredient_list5)
    add_ingredients(ingredient_list6)

    add_recipe(User.objects.get(username='tester1').user_profile, 'Teriyaki tofu with charred spring onions',
               'Main dish',
               'Cook the rice according to pack instructions. Pour the soy sauce, mirin, ginger and honey into a '
               'small saucepan and add 50ml water. Bring to a simmer and cook for around 5 mins or until slightly '
               'thickened. Remove from the heat and set aside until needed.',
               'Chinese', 'Teriyaki-tofu-with-charred-spring-onions.jpg', '25 mins', 'Easy', True, 15)

    add_recipe(User.objects.get(username='tester1').user_profile, 'Chicken pasta bake', 'Main dish',
               'Heat 2 tbsp of the oil in a pan over a medium heat and fry the onion gently for 10-12 mins. Add the '
               'garlic and chilli flakes and cook for 1 min. Tip in the tomatoes and sugar and season to taste. '
               'Simmer uncovered for 20 mins or until thickened, then stir through the mascarpone.',
               'Italian', 'Chicken-pasta-bake.jpg', '45 mins', 'Easy', False, 17)

    add_recipe(User.objects.get(username='tester1').user_profile, 'Slow cooker meatballs', 'Main dish',
               'Heat the slow cooker if necessary. Heat the oil in a non-stick frying pan and add the onion, carrots, '
               'celery and garlic and fry gently for a minute. Pour in the passata, add the parsley and stir, '
               'then transfer the lot to the slow cooker.',
               'Italian', 'Slow-cooker-meatballs.jpg', '5 hrs', 'Easy', False, 20)

    add_recipe(User.objects.get(username='tester2').user_profile, 'Guinness chocolate puddings', 'Dessert',
               'Butter four 9 x 5cm ramekins and set aside. Tip the butter, chocolate and a generous pinch of salt '
               'into a heatproof bowl. Set over a small pan of just-simmering water and stir until melted, '
               'then remove from the heat and leave to cool a little.',
               'French', 'Guinness-chocolate-puddings.jpg', '18 mins', 'Medium', True, 9)

    add_recipe(User.objects.get(username='tester2').user_profile, 'Chilli chicken & peanut pies', 'Starter',
               'Heat oven to 200C/180C fan/gas 6. Cook the potatoes in a steamer for 15 mins until tender. Meanwhile, '
               'start the chicken filling. Heat the oil in a non-stick pan, add the ginger and chilli, and stir over '
               'a medium heat until starting to soften. Stir in the dried spices, leeks and peppers. Cook, '
               'stirring frequently, until softened.',
               'American', 'Chilli-chicken-&-peanut-pies.jpg', '1 hr', 'Easy', False, 3)

    add_recipe(User.objects.get(username='tester3').user_profile, 'Vegan leek & potato soup', 'Soup',
               'Heat the oil in a large pan over a medium heat and fry the garlic and leeks, stirring, until the veg '
               'has started to soften. Add the potatoes and stock, then cover and simmer for 15 mins until the leeks '
               'and potatoes are soft.',
               'Japanese', 'Vegan-leek-&-potato-soup.jpg', '25 mins', 'Easy', True, 5)

    recipe_id_list = []
    recipe_list = Recipe.objects.all()
    for i in range(0, 5):
        recipe_id_list.append(recipe_list[i].id)
        add_bookmark(User.objects.get(username='tester'+str(i)), recipe_id_list)


def add_user(username, password, email):
    a = User.objects.get_or_create(username=username)[0]
    a.set_password(password)
    a.email = email
    a.save()
    return a


def add_user_profile(user, avatar_name):
    b = UserProfile.objects.get_or_create(user=user)[0]
    b.avatar = "/profile_images/" + avatar_name
    b.save()


def add_ingredients(name_list):
    for j in name_list:
        c = Ingredient.objects.get_or_create(name_and_amount=j)[0]
        c.save()


def add_recipe(user_profile, name, category, detail, region, photo_name, cooking_duration, difficulty, vegan, likes):
    d = Recipe.objects.get_or_create(user=user_profile, name=name, category=category, detail=detail, region=region,
                                     photo="/recipe_images/" + photo_name, cooking_duration=cooking_duration,
                                     difficulty=difficulty, is_vegan=vegan, likes=likes)[0]

    if name == 'Teriyaki tofu with charred spring onions':
        for j in ingredient_list1:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))
        add_comment(d, 'tester2', 4.0, 'Thumbs up from my wife and daughter. Used Cauldron tofu and pressed all the '
                                       'water out. The sauce in particular is so good.')
        add_comment(d, 'tester4', 4.3, 'I marinated the tofu steaks first (thin not thick- 0.4/0.5cm) and cooked them '
                                       'in my George Foreman grill with the spring onions. It needs something more, '
                                       'maybe some mushrooms/veg but I would say that this could be a stunning '
                                       'starter for a dinner and layer ingredients on top of each other for effect. '
                                       'Lots of potential- almost there.')
        add_comment(d, 'tester6', 3.5, 'Very tasty and easy to prepare!')
        add_comment(d, 'tester9', 4.2, 'Was easy to prepare. Used parboiled rice since I didn’t have whole grain '
                                       'rice. The tofu could have been marinated in some of the teriyaki sauce. The '
                                       'chive burned on the grill so I would not recommend grilling for too long. All '
                                       'in all a satisfying meal.')
    elif name == 'Chicken pasta bake':
        for j in ingredient_list2:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))
        add_comment(d, 'tester2', 4.0, 'can you freeze this')
        add_comment(d, 'tester5', 3.7, 'I did this for gcse food and it was amazing just hoped it was quicker')
        add_comment(d, 'tester7', 4.9, "I exchanged chicken for tune and added 3 red chillies (I didn't have chilli "
                                       "flakes). Really good! Very filling even stumped my 20year old lad.")

    elif name == 'Slow cooker meatballs':
        for j in ingredient_list3:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))
        add_comment(d, 'tester9', 2.0, 'Really easy and very tasty. When I make it again may add a splash of red wine '
                                       'to the sauce.')
        add_comment(d, 'tester3', 3.0, "I am going to make this and add oregano. But not sure you need the slow "
                                       "cooker on for hours as you made the sauce in a pan then fried the meatballs "
                                       "then to cook it for hours in a slow cooker? Would take less cooking time on "
                                       "the stove as you've already cooked it.")

    elif name == 'Guinness chocolate puddings':
        for j in ingredient_list4:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))
        add_comment(d, 'tester5', 5.0, 'Delish and a lot less faffy than fondants. The middle sinks into a crater '
                                       'while cooling. We scooped salted caramel ice cream into ours. Perfect.')

    elif name == 'Chilli chicken & peanut pies':
        for j in ingredient_list5:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))

    elif name == 'Vegan leek & potato soup':
        for j in ingredient_list6:
            d.ingredients.add(Ingredient.objects.get(name_and_amount=j))

    sum_, size = 0, 0
    for k in d.comments.all():
        sum_ += k.rating
        size += 1
    if size == 0:
        d.average_rating = 0
    else:
        d.average_rating = sum_ / size

    d.save()


def add_comment(recipe, username, rating, detail):
    e = Comment.objects.get_or_create(recipe=recipe, username=username, rating=rating, detail=detail)[0]
    e.save()


def add_bookmark(user, recipe_id_list):
    f = UserProfile.objects.get(user=user)
    f.bookmark = recipe_id_list
    f.save()


if __name__ == '__main__':
    populate()
    print("Finished")
