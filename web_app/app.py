"""
flask app for team 5's final project
"""
# pylint: disable=too-many-arguments
# pylint: disable=protected-access

from os import getenv
from sys import exit as sysexit
from flask import Flask, render_template, request, redirect, url_for, flash, session

# from flask_pymongo import PyMongo
from dotenv import load_dotenv
import requests

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()
app = Flask(__name__)
# app.config["MONGO_URI"] = getenv("MONGO_URI")
# mongo = PyMongo(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = getenv("FLASK_SECRET_KEY")


SPOON_SECRET = getenv("SPOON_SECRET")
if not SPOON_SECRET:
    print("Spoonacular secret not found.")
    sysexit()


def fetch_spoon_api(path: str, query: dict[str, str] = None):
    """
    Fetch from Spoonacular API.
    GET path with query string.
    Returns None when status is not OK, otherwise the parsed JSON object.
    """
    if query is None:
        query = {}
    r = requests.get(path, params={**query, "apiKey": SPOON_SECRET}, timeout=10)
    print(f"Spoonacular API - GET {r.url}")
    if r.status_code != 200:
        print(f"Spoonacular API - error:\n{r}")
        return None

    return r.json()


@app.route("/")
def index():
    """Renders home page"""
    return render_template("index.html")


# target nutrients
NUTRIENTS = {"calories", "fat", "sodium", "carbohydrates", "sugar", "protein", "fiber"}


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id=639413):
    """Renders recipe details page"""

    res = fetch_spoon_api(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        {"includeNutrition": True},
    )

    # nutrients
    nutrition = {
        nutr["name"].lower(): {
            "amt": round(nutr["amount"]),
            "units": nutr["unit"],
        }
        for nutr in res["nutrition"]["nutrients"]
        if nutr["name"].lower() in NUTRIENTS
    }
    # missing nutrients
    for nutrname in NUTRIENTS:
        if nutrname not in nutrition:
            nutrition[nutrname] = {"amt": "-", "units": "-"}

    return render_template("recipe.html", recipe=res, nutrition=nutrition)


# MongoDB setup
client = MongoClient(getenv("URI"))  # Replace with your connection string
db = client[getenv("DATABASE")]  # Replace with your database name
users = db.users
app.config['DATABASE'] = db

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    """The class User is a subclass of UserMixin."""

    def __init__(
        self,
        username,
        password,
        disliked_ingredients=None,
        saved_recipes=None,
        active=True,
        _id=None,
    ):
        """
        The function is a constructor that initializes the attributes of a user object.

        :param username: The username parameter is used to store the username of the user
        :param password: The `password` parameter is used to store the password for the user
        :param active: The "active" parameter is a boolean value that indicates whether the user is
        currently active or not. By default, it is set to True, meaning the user is active, defaults
        to True (optional)
        :param _id: The `_id` parameter is used to store a unique identifier for the object. It is
        an optional parameter and can be set to `None` if no identifier is provided
        """
        self.username = username
        self.password = password
        self.active = active
        self._id = _id
        self.disliked_ingredients = disliked_ingredients
        self.saved_recipes = saved_recipes

    def get_id(self):
        """
        The function returns the username as the ID.
        :return: The username of the object.
        """
        return self.username

    @property
    def is_active(self):
        """
        The function returns the value of the "active" attribute.
        :return: The method is returning the value of the attribute "active".
        """
        return self.active


@login_manager.user_loader
def load_user(username):
    """
    The function `load_user` retrieves user information from a database and returns a `User` object.

    :param username: The username parameter is the username of the user we want to load from the
    database
    :return: an instance of the User class with the specified attributes.
    """
    u = users.find_one({"username": username})
    if not u:
        return None
    return User(
        username=u["username"],
        password=u["password"],
        disliked_ingredients=u.get("disliked_ingredients"),
        saved_recipes=u.get("saved_recipes"),
        _id=u["_id"],
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    The `signup` function handles the user registration process. It accepts user input from a form,
    validates it, and then creates a new user in the database.
    :return: either a redirect to the "index" page or rendering the "signup.html" template.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Check if user already exists
        if users.find_one({"username": username}):
            flash("Username already exists.")
            return redirect(url_for("signup"))

        # Create new user
        hashed_password = generate_password_hash(password)
        users.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful.")
        return redirect(url_for("main"))  # Redirect to the main page
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The `login` function checks if the user's credentials are valid and logs them in if they are,
    otherwise it displays an error message.
    :return: either a redirect to the "index" page or rendering the "login.html" template.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_doc = users.find_one({"username": username})
        # if user_doc and check_password_hash(user_doc["password"], password):
        #     user = User(username=user_doc["username"], password=user_doc["password"])
        #     login_user(user)
        #     return redirect(url_for("index"))
        if user_doc and check_password_hash(user_doc["password"], password):
            user = User(username=user_doc["username"], password=user_doc["password"])
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main"))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """
    The function "logout" logs out the user and redirects them to the index page.
    :return: a redirect to the "index" route.
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/main")
@login_required
def main():
    """
    The main function retrieves the value of the "recipes" key from the session dictionary and
    sets it to an empty list if the key is not present, then renders the "main.html" template
    with the current user's username and the recipes.
    :return: the rendered template "main.html" with the variables "username" set to the
    current user's username and "recipes" set to the value of the "recipes" key from the session
    dictionary. If the "recipes" key is not present in the session dictionary, it will
    be set to an empty list.
    """
    # retrieves the value of the "recipes" key from the session dictionary.
    # If the key is not present in session, it sets the value to an empty list.
    recipes = session.get("recipes", [])
    session.pop("recipes", None)

    return render_template("main.html", username=current_user.username, recipes=recipes)


@app.route("/set_preferences", methods=["POST"])
@login_required
def set_preferences():
    """
    The `set_preferences` function takes user input for disliked ingredients, combines it with the
    user's current disliked ingredients, removes duplicates, and updates the user's preferences
    in the database.
    :return: a redirect to the "main" route.
    """
    new_disliked_ingredients = request.form.get("disliked_ingredients", "").strip()
    new_disliked_ingredients_list = [
        ingredient.strip() for ingredient in new_disliked_ingredients.split(",")
    ]
    print("new_disliked_ingredients_list", new_disliked_ingredients_list)

    # Fetch current user's disliked ingredients from db
    user_preferences = users.find_one({"_id": current_user._id})
    current_disliked_ingredients = user_preferences.get("disliked_ingredients", "")
    print("current_disliked_ingredients", current_disliked_ingredients)

    # convert the existing string to a list, remove empty strings if any
    current_disliked_ingredients_list = [
        ingredient
        for ingredient in current_disliked_ingredients.split(",")
        if ingredient
    ]

    # combine the lists, remove duplicates, and convert back to a string
    updated_disliked_ingredients_list = list(
        set(current_disliked_ingredients_list + new_disliked_ingredients_list)
    )
    updated_disliked_ingredients = ",".join(updated_disliked_ingredients_list)

    print("updated_disliked_ingredients", updated_disliked_ingredients)

    users.update_one(
        {"_id": current_user._id},
        {"$set": {"disliked_ingredients": updated_disliked_ingredients}},
    )
    # print("current_user.disliked_ingredients:", current_user.disliked_ingredients)

    return redirect(url_for("main"))


@app.route("/show_recipes", methods=["POST"])
@login_required
def show_recipes():
    """
    The function fetches recipes from the Spoonacular API, excluding any ingredients
    that the current user has disliked, and stores the recipes in the session.
    :return: a redirect to the "main" route.
    """
    # Fetch current user's disliked ingredients from db
    user_preferences = users.find_one({"_id": current_user._id})
    disliked_ingredients = user_preferences.get("disliked_ingredients", "")

    recipes = fetch_spoon_api(
        "https://api.spoonacular.com/recipes/complexSearch",
        {"excludeIngredients": disliked_ingredients, "number": "6"},
    ).get("results", [])

    # Store recipes in session
    session["recipes"] = recipes

    return redirect(url_for("main"))


@app.route("/save_recipe", methods=["POST"])
@login_required
def save_recipe():
    """
    The `save_recipe` function saves a recipe by adding its ID to the `saved_recipes` array of the
    current user.
    :return: a dictionary with two key-value pairs. The "status" key has the value "success" and the
    "message" key has the value "Recipe saved".
    """
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    users.update_one(
        {"_id": current_user._id}, {"$addToSet": {"saved_recipes": recipe_id}}
    )
    return {"status": "success", "message": "Recipe saved"}


# @app.route("/search_results")
# @login_required
# def search_results():
#     """Renders search results page"""
#     disliked_ingredients = current_user.disliked_ingredients
#     recipes = fetch_spoon_api(
#         "https://api.spoonacular.com/recipes/complexSearch",
#         {"excludeIngredients": disliked_ingredients, "number": "5"},
#     )

#     return render_template("search_results.html", recipes=recipes["results"])


# @app.route("/remove_preference/<ingredient>", methods=["POST"])
# @login_required
# def remove_preference(ingredient):
#     users.update_one(
#         {"_id": current_user._id},
#         {"$pull": {"disliked_ingredients": ingredient}},
#     )
#     return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True, debug=True)
