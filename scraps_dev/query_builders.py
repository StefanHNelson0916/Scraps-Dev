from werkzeug.security import check_password_hash, generate_password_hash

def get_db_table(dish_type):
    if dish_type == 'MainDish' or dish_type == 'Main Dish':
        return 'md'
    elif dish_type == 'SideDish' or dish_type == 'Side Dish':
        return 'sd'
    elif dish_type == 'Dessert':
        return 'ds'

def get_order_by_values(order_by, dish_type):
    table = get_db_table(dish_type)
    dropdown_value_to_table = {
        'aToZ' : 'recipe_name ASC',
        'zToA' : 'recipe_name DESC',
        'ingredientsHigh' : f'{table}_counts.ingredient_count DESC',
        'ingredientsLow' : f'{table}_counts.ingredient_count ASC',
        'stepsHigh' : f'{table}_counts.step_count DESC',
        'stepsLow' : f'{table}_counts.step_count ASC'
    }
    return dropdown_value_to_table[order_by]

def get_dropdown_text(order_type):
    order_type_dict = {
        'aToZ' : 'A - Z',
        'zToA' : 'Z - A',
        'ingredientsHigh' : 'Ingredients: High',
        'ingredientsLow' : 'Ingredients: Low',
        'stepsHigh' : 'Steps: High',
        'stepsLow' : 'Steps: Low'
    }
    return order_type_dict[order_type]

def first_part(rest_of_query, table, order_by):
    return f'''
    SELECT 
        {table}_recipes.recipe_id, 
        {table}_recipes.recipe_name, 
        {table}_counts.step_count, 
        {table}_counts.ingredient_count
    FROM (
    {rest_of_query}
    ) AS subquery
    JOIN  {table}_counts ON subquery.recipe_id = {table}_counts.recipe_id
    JOIN {table}_recipes ON subquery.recipe_id = {table}_recipes.recipe_id
    ORDER BY {order_by}
    LIMIT 100
    '''

def middle_part(ingredient, rest_of_query):
    return f'''
    SELECT * 
    FROM (
    {rest_of_query}
    ) AS subquery
    WHERE subquery.recipe_ingredients
    LIKE "%{ingredient}%"
    '''

def last_part(ingredient,table):
    return f'''
    SELECT * 
    FROM {table}_ingredients 
    WHERE recipe_ingredients 
    LIKE "%{ingredient}%"
    '''

def single_ingredient(ingredient, table, order_by):
    return f'''
    SELECT 
        {table}_recipes.recipe_id, 
        {table}_recipes.recipe_name, 
        {table}_counts.step_count, 
        {table}_counts.ingredient_count
    FROM {table}_ingredients
    JOIN {table}_recipes ON {table}_recipes.recipe_id = {table}_ingredients.recipe_id
    JOIN  {table}_counts ON {table}_recipes.recipe_id = {table}_counts.recipe_id
    WHERE recipe_ingredients
    LIKE "%{ingredient}%"
    ORDER BY {order_by}
    LIMIT 100
    '''

def get_recipes_by_ingredient(dish_type, ingredients, order_by):
    ingredients = ingredients.split('+')
    table = get_db_table(dish_type)
    order_by = get_order_by_values(order_by, dish_type)

    query = ''

    if len(ingredients) == 1:
        query = single_ingredient(ingredients[0], table, order_by)
        return query

    i = 0
    for ingredient in reversed(ingredients):
        if i == 0:
            query = last_part(ingredient, table)
        else:
            query = middle_part(ingredient, query)
        i += 1
    query = first_part(query, table, order_by)

    return query

def ingredients_recipe_count_query(ingredients, dish_type):
    ingredients = ingredients.split('+')
    db_table = get_db_table(dish_type)
    i = 0
    for ingredient in ingredients:
        if i == 0 and (len(ingredients) > 1):
            query = f'SELECT * FROM {db_table}_ingredients WHERE recipe_ingredients LIKE "%{ingredient}%"'
        elif (i == 0):
            query = f'SELECT COUNT(*) FROM {db_table}_ingredients WHERE recipe_ingredients LIKE "%{ingredient}%"'
        elif i == len(ingredients) - 1:
            query = f'SELECT COUNT(*) FROM ({query}) AS subquery WHERE subquery.recipe_ingredients LIKE "%{ingredient}%"'
        else: 
            query = f'SELECT * FROM ({query}) AS subquery WHERE subquery.recipe_ingredients LIKE "%{ingredient}%"'
        i += 1
    return query      

def get_ingredients(recipe_id, dish_type):
    db_table = get_db_table(dish_type)
    return f'SELECT recipe_ingredients FROM {db_table}_ingredients WHERE recipe_id = {recipe_id}'

def get_tags(recipe_id, dish_type):
    db_table = get_db_table(dish_type)
    return f'SELECT recipe_tags FROM {db_table}_tags WHERE recipe_id = {recipe_id}'

def get_steps(recipe_id, dish_type):
    db_table = get_db_table(dish_type)
    return f'SELECT recipe_steps FROM {db_table}_steps WHERE recipe_id = {recipe_id}'

def add_user():
    return f'INSERT INTO users (username, password) VALUES (%s, %s)'

def get_user_by_username(username):
    return f'SELECT * FROM users WHERE username = "{username}"'

def get_user_by_id(user_id):
    return f'SELECT * FROM users WHERE id = {user_id}'

def get_user_history(user_id):
    return f'SELECT * FROM user_history WHERE user_id = {user_id};'

def get_user_saved(user_id):
    return f'''
    SELECT * 
    FROM user_saved
    WHERE user_saved.user_id = {user_id};
    '''

def get_recipe(id, dish_type):
    print(f'dish type : {dish_type}')
    table = get_db_table(dish_type)
    print(f'table :  {table}')
    return f'''
    SELECT {table}_recipes.recipe_id, {table}_recipes.recipe_name, {table}_ingredients.recipe_ingredients, {table}_steps.recipe_steps, {table}_tags.recipe_tags
    FROM {table}_recipes
    JOIN {table}_ingredients ON {table}_recipes.recipe_id = {table}_ingredients.recipe_id
    JOIN {table}_steps ON {table}_recipes.recipe_id = {table}_steps.recipe_id
    JOIN {table}_tags ON {table}_recipes.recipe_id = {table}_tags.recipe_id
    WHERE {table}_recipes.recipe_id = {id};
    '''

def get_history_items(user_id):
    return f'''
    SELECT DISTINCT *
    FROM user_history
    WHERE user_id = {user_id}
    ORDER BY occurred_at DESC
    '''

def get_history_item(history_item_id):
    return f'''
    SELECT *
    FROM user_history
    WHERE history_item_id = {history_item_id}
    '''

def unsave_recipe(user_id, recipe_id):
    return f'''
    DELETE
    FROM user_saved
    WHERE user_id = {user_id} AND recipe_id = {recipe_id}
    ;
    '''

def save_recipe(user_id, recipe_id, dish_type, recipe_name):
    return f'''
    INSERT INTO user_saved (user_id, recipe_id, dish_type, recipe_name)
    VALUES ({user_id},{recipe_id},'{dish_type}','{recipe_name}')
    '''

def check_recipe_saved(user_id, recipe_id):
    return f'''
    SELECT *
    FROM user_saved
    WHERE user_id = {user_id} AND
    recipe_id = {recipe_id}
    '''

def add_user_history_item(user_id, item_type, dish_type, item_content, occurred_at):
    return f'''
    INSERT INTO user_history (user_id, item_type, dish_type, item_content, occurred_at)
    VALUES ({user_id}, '{item_type}', '{dish_type}', '{item_content}', '{occurred_at}')
    '''

def get_recipes_with_tag(tag, dish_type, order_by):
    table = get_db_table(dish_type)
    order_type  = get_order_by_values(order_by, dish_type)
    return f'''
    SELECT 
    {table}_recipes.recipe_id, 
    {table}_recipes.recipe_name, 
    {table}_counts.step_count, 
    {table}_counts.ingredient_count
    FROM {table}_tags
    JOIN {table}_recipes ON {table}_tags.recipe_id = {table}_recipes.recipe_id
    JOIN {table}_counts ON {table}_tags.recipe_id = {table}_counts.recipe_id
    WHERE {table}_tags.recipe_tags
    LIKE "%'{tag}'%"
    ORDER BY {order_type}
    LIMIT 100;
    '''

def string_recipe_count_query(dish_type, name):
    table = get_db_table(dish_type)
    return f'''
    SELECT COUNT(*)
    FROM {table}_recipes
    WHERE recipe_name
    LIKE '%{name}%';
    '''

def recipes_by_string_query(string, dish_type, order_by):
    table = get_db_table(dish_type)
    order_type = get_order_by_values(order_by, dish_type)
    return f'''
    SELECT
    {table}_recipes.recipe_id, 
    {table}_recipes.recipe_name, 
    {table}_counts.step_count, 
    {table}_counts.ingredient_count
    FROM {table}_recipes
    JOIN {table}_counts ON {table}_recipes.recipe_id = {table}_counts.recipe_id 
    WHERE recipe_name
    LIKE '%{string}%'
    ORDER BY {order_type}
    LIMIT 100;
    '''

def check_already_in_history(user_id, item_type, item_content, dish_type):
    print(f'at qb : {user_id}, {item_type}, {item_content}, {dish_type}')
    return f'''
    SELECT *
    FROM user_history
    WHERE user_id = {user_id} AND
    item_type = "{item_type}" AND
    item_content = "{item_content}" AND
    dish_type = "{dish_type}";
    '''