
from flask import Flask, render_template, request
import spoonacular as sp
import os
from pprint import pformat
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
API_KEY = os.environ['SPOONACULAR_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/recipes')
def get_recipes():
    """Get recipes by ingredients"""

    ingredients = request.args.get("ingredients")
    print("******Input Ingredients:*****", ingredients)

    #ingredients = ["chicken", "pasta", "butter"]
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    payload = {'ingredients': ingredients, 'number': 10, 'apiKey': API_KEY}

    response = requests.get(url, params=payload)

    if response.status_code != 200:
                response.raise_for_status()
    
    recipes = response.json()

    #print(recipes)
    #for recipe in recipes:
    #    print (recipe['title'])

    return render_template('recipes.html', recipes=recipes)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
