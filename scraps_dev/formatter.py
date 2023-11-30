from scraps_dev.schema import  Recipe

def db_recipes_to_dict_list(db_recipes, dish_type, ingredients=None):
    recipes = []
    for recipe in db_recipes:
        recipe = Recipe(id=recipe[0], name=recipe[1], dish_type=dish_type, step_count=recipe[2], ingredient_count=recipe[3], ingredients=ingredients)
        recipes.append(vars(recipe))
    return recipes

def get_dish_type_text(dish_type):
    if dish_type == "MainDish":
        return "Main Dish"
    elif dish_type == "SideDish":
        return "Side Dish"
    elif dish_type == "Dessert":
        return "Dessert"
    else:
        return dish_type