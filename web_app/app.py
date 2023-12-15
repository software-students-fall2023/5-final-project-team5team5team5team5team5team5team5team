"""
flask app for team 5's final project
"""

from os import getenv
from sys import exit as sysexit
from flask import Flask, render_template, request, redirect, url_for, flash, session
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

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    """The class User is a subclass of UserMixin."""

    def __init__(self, username, password, active=True, _id=None):
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

    def get_id(self):
        """
        The function returns the username as the ID.
        :return: The username of the object.
        """
        return self.username

    @property
    def is_active(self):
        return self.active


@login_manager.user_loader
def load_user(username):
    """
    The function `load_user` loads a user from a database based on their username and returns a
    `User`object.

    :param username: The `username` parameter is a string that represents the username of the
    user we want to load from the database
    :return: an instance of the User class with the specified username, password, and _id.
    """
    u = users.find_one({"username": username})
    if not u:
        return None
    return User(username=u["username"], password=u["password"], _id=u["_id"])


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
@login_required  # Require the user to be logged in to view the main page
def main():
    """Renders the main page"""
    print("Current session:", session)
    return render_template("main.html", username=current_user.username)


if __name__ == "__main__":
    app.run(use_reloader=True)
