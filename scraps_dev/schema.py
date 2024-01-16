class Recipe:
    def __init__(self, id, dish_type, name, ingredients=None, ingredient_count=None, steps=None, step_count=None, tags=None):
        self.id =  id
        self.dish_type = dish_type
        self.name = name.capitalize()
        self.ingredients = ingredients
        if self.ingredients is not None:
            if type(self.ingredients) is str:
                self.ingredients = recipe_ingredients_string_to_list(ingredients)
        self.ingredient_count = ingredient_count
        if self.ingredients is not None and self.ingredient_count is not None:
            self.missing_ingredients = ingredient_count - len(self.ingredients)
        else:
            self.missing_ingredients = None
        self.step_count = step_count
        self.steps = steps
        if self.steps is not None:
            self.steps = recipe_ingredients_string_to_list(steps)
        self.tags = tags
        if self.tags is not None:
            self.tags = recipe_ingredients_string_to_list(tags)

def recipe_ingredients_string_to_list(string):
    string = string.replace('[','').replace(']','')
    string = string[1:-1]
    string_elements = string.split("', '")
    string_elements = [item.capitalize() for item in string_elements]
    return string_elements

class HistoryItem:
    def __init__(self, values):
        self.action_id = values['history_item_id']
        self.action_type = item_types_string_formatter(item_types=values['item_type'], dish_type=values['dish_type'])
        self.action_content = values['item_content']
        self.dish_type = values['dish_type']

        if (len(self.action_content.split('@')) > 1):
            self.recipe_id = self.action_content.split('@')[1]
            self.action_content = self.action_content.split('@')[0] 
        else:
            self.recipe_id = None

        self.occurred_at = values['occurred_at'].date().strftime("%m-%d-%Y")

def item_types_string_formatter(item_types : str, dish_type : str) -> str:
    item_types : list = item_types.split(':')
    history_action_type : str = item_types[0]
    search_action_type : str = item_types[1].lower()
    if history_action_type == 'Searched':
        display_text: str = f'{dish_type} with {search_action_type}'
        return display_text