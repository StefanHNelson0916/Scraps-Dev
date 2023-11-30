from flask import Blueprint, render_template, redirect, url_for, g, session
from datetime import datetime
import scraps_dev.db as db
import scraps_dev.query_builders as qb
import scraps_dev.formatter as ft
from scraps_dev.schema import HistoryItem

bp = Blueprint("search", __name__, url_prefix="/Search")

@bp.route("/Ingredients")
def ingredients_search():
    return render_template("ingredients_search_bar.html")

@bp.route("/String")
def string_search():
    return render_template("string_search.html")

@bp.route("/RecipeCount/<search_type>/<search_input>/<dish_type>")
def recipe_count(search_type, search_input, dish_type):
    if search_type == "Ingredients":
        recipe_count = db.get_ingredients_recipe_count(ingredients=search_input, dish_type=dish_type)
    elif search_type == "String":
        recipe_count = db.get_string_recipe_count(string=search_input, dish_type=dish_type)
    recipe_count = str(recipe_count[0])
    return (recipe_count)

@bp.route("/Results/<search_type>/<search_input>/<dish_type>", defaults={'order_by':'aToZ'})
@bp.route("/Results/<search_type>/<search_input>/<dish_type>/<order_by>")
def results(search_type, search_input, dish_type, order_by):
    if search_type == 'Ingredients':
        db_recipes = db.get_recipes_by_ingredient(dish_type, search_input, order_by=order_by)
        recipes = ft.db_recipes_to_dict_list(db_recipes, dish_type, ingredients=search_input)
        order_by = qb.get_dropdown_text(order_by)
        dish_type = ft.get_dish_type_text(dish_type)
        title = f'{dish_type} with Ingredients ({search_input})'
    elif search_type == 'String':
        db_recipes = db.get_recipes_by_string(search_input, dish_type, order_by)
        recipes = ft.db_recipes_to_dict_list(db_recipes, dish_type)
        order_by = qb.get_dropdown_text(order_by)
        dish_type = ft.get_dish_type_text(dish_type)
        title = f'{dish_type} with "{search_input}"'
    elif search_type == 'Tag':
        db_recipes = db.get_recipes_by_tag(search_input, dish_type, order_by)
        recipes = ft.db_recipes_to_dict_list(db_recipes, dish_type)
        order_by = qb.get_dropdown_text(order_by)
        dish_type = ft.get_dish_type_text(dish_type)
        title = f'{dish_type} with Tag [{search_input}]'
    if len(recipes) != 0:
        user_id = session.get('user_id')
        if user_id is not None:
            item_values : list = [user_id, search_type, search_input, dish_type]
            add_user_history_item(item_values)
    return render_template(
        'search_results.html',
        title=title,
        search_type=search_type,
        recipes=recipes,
        search_input=search_input,
        dish_type=dish_type,
        order_by=order_by
        )

@bp.route("/OrderResults/<search_type>/<search_input>/<dish_type>/<order_by>")
def order_results(search_type, search_input, dish_type, order_by):
    if search_type == 'Tag':
        return redirect(url_for('search.results', search_type='Tag', search_input=search_input, dish_type=dish_type, order_by=order_by))
    if search_type == 'Ingredients':
        return redirect(url_for('search.results', search_type='Ingredients', search_input=search_input, dish_type=dish_type, order_by=order_by))
    if search_type == 'String':
        return redirect(url_for('search.results', search_type='String', search_input=search_input, dish_type=dish_type, order_by=order_by))

@bp.route("/HistoryItem/<item_id>")
def history_item(item_id):
    user_id : int = session.get('user_id')
    print(f'user_id : {user_id}')
    print(f'item_id : {item_id}')
    history_item  = db.get_history_item(item_id)
    item_types : list = history_item[2].split(':')
    print(item_types)
    if item_types[0] == 'Searched':
        return redirect(
            url_for(
                'search.results',
                search_type=item_types[1],
                search_input=history_item[3],
                dish_type=history_item[4]
            )
        )
    return item_id

def add_user_history_item(item_values : list):
    occurred_at = datetime.now()
    history_item = HistoryItem(item_values)
    print(history_item)
    # in_history = db.check_already_in_history(
    #     user_id=user_id,
    #     item_type=search_type,
    #     item_content=search_input,
    #     dish_type=dish_type
    # )
    # if not in_history:
    #     db.add_user_history_item(
    #         user_id,
    #         search_type,
    #         dish_type, search_input, occurred_at)