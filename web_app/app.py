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

@app.route("/recipe/<recipe_id>")
def recipe(recipe_id=639413):
    res = fetch_spoon_api(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        { "includeNutrition": True }
    )
    print(res)
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
