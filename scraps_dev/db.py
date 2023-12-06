import scraps_dev.query_builders as qb
import mysql.connector
from mysql.connector import Error
from datetime import datetime

db = mysql.connector.connect(
    host="localhost", user="root", password="", database="scraps_dev"
)


def get_one(query):
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def get_all(query):
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def add_item(query):
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()


def add_user(query, values):
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()


def get_ingredients_recipe_count(ingredients, dish_type):
    query = qb.ingredients_recipe_count_query(
        ingredients=ingredients, dish_type=dish_type
    )
    recipe_count = get_one(query)
    return recipe_count


def get_recipes_by_ingredient(dish_type, ingredients, order_by):
    query = qb.get_recipes_by_ingredient(dish_type, ingredients, order_by)
    recipes = get_all(query=query)
    return recipes


def get_recipe(recipe_id, dish_type):
    query = qb.get_recipe(recipe_id, dish_type)
    result = get_one(query)
    return result


def get_history_items(user_id):
    query = qb.get_history_items(user_id)

    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    field_names = [column[0] for column in cursor.description]
    result = [dict(zip(field_names, row)) for row in result]

    cursor.close()
    db.close()

    return result


def get_history_item(item_id):
    query = qb.get_history_item(item_id)
    result = get_one(query)
    return result


def save_recipe(user_id, recipe_id, dish_type, dish_name):
    try:
        # Establish a connection to the MySQL server
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="scraps_dev"
        )

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Your SQL query
        query = qb.save_recipe(user_id, recipe_id, dish_type, dish_name)

        # Execute the query
        cursor.execute(query)

        # Commit the changes
        db.commit()

    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate key error
            print("Duplicate key error. Handle accordingly.")
        else:
            print(f"Error: {err}")

    finally:
        # Close the cursor and connection in the finally block
        if db.is_connected():
            cursor.close()
            db.close()


def unsave_recipe(user_id, recipe_id):
    query = qb.unsave_recipe(user_id, recipe_id)

    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )

    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()


def check_recipe_saved(user_id, recipe_id):
    query = qb.check_recipe_saved(user_id, recipe_id)

    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="scraps_dev"
    )

    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


def add_user_history_item(values):
    query = qb.add_user_history_item(values)
    add_item(query)


def get_recipes_by_tag(tag, dish_type, order_by):
    query = qb.get_recipes_with_tag(tag, dish_type, order_by)
    recipes = get_all(query)
    return recipes


def get_string_recipe_count(dish_type, string):
    query = qb.string_recipe_count_query(dish_type, string)
    recipe_count = get_one(query)
    return recipe_count


def get_recipes_by_string(string, dish_type, order_by):
    query = qb.recipes_by_string_query(string, dish_type, order_by)
    recipes = get_all(query)
    return recipes


def check_already_in_history(values):
    query = qb.check_already_in_history(values)
    recipes = get_all(query)
    if len(recipes) > 0:
        return True
    else:
        return False