from flask import  (
    Blueprint, flash, g, redirect, render_template, request, session, jsonify, url_for
)
import scraps_dev.db as db
from scraps_dev.schema import Recipe
from datetime import datetime

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route("/page/<recipe_id>/<dish_type>")
def page(recipe_id, dish_type):
    recipe_values = db.get_recipe(recipe_id, dish_type)
    recipe = Recipe(id=recipe_values[0], name=recipe_values[1], dish_type=dish_type, ingredients=recipe_values[2], steps=recipe_values[3], tags=recipe_values[4])
    recipe = vars(recipe)

    # user_id = session.get("user_id")
    # if user_id is not None:
    #     action_type = 'Viewed Recipe'
    #     action_content = recipe_name  + '@' + str(recipe_id)
    #     occurred_at = datetime.now().date()
    #     db.add_user_history_item(user_id, action_type, dish_type, action_content, occurred_at)  
    return render_template("recipe_page.html", recipe=recipe, dish_type=dish_type)

@bp.route("/saved_recipe_page/<recipe_id>/<dish_type>/<name>")
def get_saved_recipe(recipe_id, dish_type, name):
    recipe_values = db.get_recipe(recipe_id, dish_type)
    recipe = Recipe(recipe_values[0], dish_type, recipe_values[1])
    recipe.set_values(recipe_values)
    recipe = vars(recipe)

    return render_template(
        "recipe_page.html", recipe=recipe
    )

@bp.route("/check_saved/<recipe_id>", methods=["GET"])
def check_saved(recipe_id):
    data = recipe_id
    if session.get("user_id"):
        user_id = session.get("user_id")
        check_result = db.check_recipe_saved(user_id=user_id, recipe_id=recipe_id)
        if check_result:
            data = 1
        else:
            data = 0
    return jsonify(data)

@bp.route("/save_recipe", methods=["POST"])
def save_recipe():
    '''
    data = {
        recipe_id: "{{ recipe['id'] }}",
        dish_type: "{{ recipe['dish_type'] }}",
        recipe_name: "{{ recipe['name'] }}"
    }
    '''
    data = request.get_json()
    user_id = g.user[0]

    db.save_recipe(user_id, data['recipe_id'], data['dish_type'], data['recipe_name'])
    
    return jsonify({'message': f'Recipe Saved {data['recipe_id']}'})

@bp.route("/unsave_recipe", methods=["POST"])
def unsave():
    '''
    data = {
        recipe_id: "{{ recipe['id'] }}",
        from_page: "profile" OR "recipe"
    }
    '''
    user_id = g.user[0]
    data = request.get_json()
    db.unsave_recipe(user_id, data['recipe_id'])
    if data['from_page'] == 'profile':
        return redirect(url_for('profile'))
    else:
        return jsonify({'message': f'Recipe Unsaved {data['recipe_id']}'})