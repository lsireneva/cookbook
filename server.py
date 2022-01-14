
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

    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    payload = {'ingredients': ingredients, 'number': 10, 'apiKey': API_KEY}

    response = requests.get(url, params=payload)

    if response.status_code != 200:
                response.raise_for_status()
    
    recipes = response.json()

    #print(recipes)
    # for recipe in recipes:
    #     print (recipe['title'])
    #     print(recipe["usedIngredients"])

    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes_advanced')
def get_recipes_advanced():
    
    query = request.args.get("query")
    print("******Input Dish:*****", query)

    includeIngredients = request.args.get("includeIngredients")
    print("******Input Ingredients:*****", includeIngredients)

    cuisine = request.args.get("cuisine")
    print("******Cuisine:*****", cuisine)

    diet = request.args.get("diet")
    print("******Diet:*****", diet)

    meal_type = request.args.get("type")
    print("******Meal type:*****", meal_type)

    values = request.args.getlist('intolerances') 
    
    intolerances =",".join(values)
    print ("******Intolerances:*****", intolerances)

    url = 'https://api.spoonacular.com/recipes/complexSearch'
    payload = {'query': query,
                'cuisine': cuisine,
                'diet': diet,  
                'intolerances': intolerances,
                'includeIngredients': includeIngredients,
                'type': meal_type,
                'addRecipeInformation': True,
                'number': 1, 
                'apiKey': API_KEY}

    response = requests.get(url, params=payload)
    print ("response:", response)

    if response.status_code != 200:
                response.raise_for_status()
    
    recipes = response.json()

    print(recipes)
    # for recipe in recipes:
    #     print (recipe['title'])
    #     print(recipe["usedIngredients"])

    return render_template('recipes_advanced.html', recipes=recipes)


@app.route('/recipe_details/<recipe_id>')
def get_recipe_details(recipe_id):
    
    print("******recipe_id=",recipe_id)

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    payload = {'includeNutrition': True, 'apiKey': API_KEY}

    response = requests.get(url, params=payload)
    print ("response:", response)

    if response.status_code != 200:
        response.raise_for_status()
    
    recipe_details = response.json()

    summary = recipe_details['summary'].replace("</b>", "").replace("<b>", "")
    test = summary.split('.')
    print("Summary", summary)
    print("Test", test)
    return render_template('recipe_details.html', recipe=recipe_details, summary=summary)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
