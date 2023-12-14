"""
flask app for team 5's final project
"""

from os import getenv
from flask import Flask, render_template
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)


SPOON_SECRET = getenv("SPOON_SECRET")
if not SPOON_SECRET:
    print("Spoonacular secret not found.")
    exit()

def fetch_spoon_api(path: str, query: dict[str, str]=None):
    """
    Fetch from Spoonacular API.
    GET path with query string.
    Returns None when status is not OK, otherwise the parsed JSON object.
    """
    if query is None:
        query = {}
    r = requests.get(path, params={**query, "apiKey": SPOON_SECRET})
    print(f"Spoonacular API - GET {r.url}")
    if r.status_code != 200:
        print(f"Spoonacular API - error:\n{r}")
        return None
    else:
        return r.json()


@app.route("/")
def index():
    """Renders home page"""
    return render_template("index.html")

# target nutrients
NUTRIENTS = {"Calories", "Fat", "Sodium", "Carbohydrates", "Sugar", "Protein", "Fiber"}
@app.route("/recipe/<recipe_id>")
def recipe(recipe_id=639413):
    from recipe_test_res import RECIPE_TEST_RES
    # res = fetch_spoon_api(
    #     f"https://api.spoonacular.com/recipes/{recipe_id}/information",
    #     { "includeNutrition": True }
    # )
    res = RECIPE_TEST_RES
    nutrition = {
        nutr["name"].lower(): {
            "amt": round(nutr["amount"]),
            "units": nutr["unit"],
        }
        for nutr in res["nutrition"]["nutrients"]
        if nutr["name"] in NUTRIENTS
    }
    return render_template("recipe.html", recipe=res, nutrition=nutrition)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
