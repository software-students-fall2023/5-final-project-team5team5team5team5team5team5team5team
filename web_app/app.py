"""
flask app for team 5's final project
"""

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


def fetch_spoon_api():
    """fetch from Spoonacular API"""
    pass   


@app.route("/")
def index():
    """Renders home page"""
    return render_template("index.html")

@app.route("/recipe/<recipe_id>")
def recipe(recipe_id=639413):
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
