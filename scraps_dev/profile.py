from flask import  (
    Blueprint, flash, g, redirect, render_template, request, session, jsonify, url_for
)
import scraps_dev.db as db
import scraps_dev.query_builders as qb
from scraps_dev.schema import Recipe, HistoryItem

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route("/")
def profile():
    user_history = db.get_history_items(g.user[0])
    user_saved = qb.get_user_saved(g.user[0])
    user_saved = db.get_all(user_saved)

    history_items : list = []
    for item_values in user_history:
        history_item : HistoryItem = HistoryItem(item_values)
        history_item_dict : dict = vars(history_item)
        history_items.append(history_item_dict)

    saved_recipes : list = []
    for recipe in user_saved:
        recipe : Recipe = Recipe(recipe[1], recipe[2], recipe[3])
        saved_recipes.append(recipe)

    return render_template(
        "profile.html", 
        user_history=history_items,
        saved_recipes=saved_recipes
    )

@bp.route("/history_item/<action_id>")
def get_history_item(action_id):
    history_item = HistoryItem(db.get_user_history_item(action_id))
    action_type = history_item.action_type

    if action_type == "Searched With Ingredients":
        ingredients = history_item.action_content
        ingredients = ingredients.split('+')
        if "ingredients" in session.keys():
            session.pop("ingredients", None)
        session["ingredients"] = ingredients
        if "dish_type" in session.keys():
            session.pop("dish_type", None)
        session["dish_type"] = history_item.dish_type
        return redirect(
            url_for(
                "search.search_results", 
                search_from='profile'
            )
        )
    elif action_type == "Viewed Recipe":
        dish_type = dish_type
        recipe_id = history_item.recipe_id
        recipe_name = history_item.recipe_name
        return redirect(
            url_for(
                "recipe.get_saved_recipe",
                recipe_id=recipe_id,
                dish_type=dish_type,
                name=recipe_name
                )
            )
    
@bp.route("/unsave/<recipe_id>")
def unsave_recipe(recipe_id):
    user_id = g.user[0]
    recipe_id = recipe_id
    db.unsave_recipe(user_id, recipe_id)
    return redirect(url_for('profile.profile'))