"""
flask app for team 5's final project
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Renders home page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
