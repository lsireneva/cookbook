
from flask import Flask, render_template, request, flash, redirect, session
import spoonacular as sp
import os
import json
from pprint import pformat
import requests
import model
import crud


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
API_KEY = os.environ['SPOONACULAR_KEY']
model.connect_to_db(app)

# Load movie data from JSON file
#with open("data/recipe_information.json") as f:
#    recipe_info = json.loads(f.read())

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/signup')
def signup():

    """Registration form for new users"""

    return render_template('signup.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    """Create user account"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.add_new_user(fname,lname,email,password):
        print('New user account created', 'message')
    else:
        print('User creation failed', 'error')
    return redirect('/')


@app.route('/login')
def login():
    """User login page"""

    return render_template('login.html')

@app.route('/check_login', methods=['POST'])
def check_login():

    email = request.form.get('email')
    password = request.form.get('password')
    print ("email", email)
    print("password", password)

    user = crud.check_login(email, password)
    print ("USER:", user)
    
    
    if user:
        session['user_id'] = user.user_id
        return redirect('/')
    else:
        print('ERORR', 'User login failed')
        return redirect('/login')


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
                'number': 5, 
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

    """Do not delete commented code"""
    
    print("******recipe_id=",recipe_id)

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    payload = {'includeNutrition': True, 'apiKey': API_KEY}

    response = requests.get(url, params=payload)
    print ("response:", response)

    if response.status_code != 200:
        response.raise_for_status()
    
    recipe_info = response.json()

    # summary = recipe_details['summary'].replace("</b>", "").replace("<b>", "")
    # test = summary.split('.')
    # print("Summary", summary)
    # print("Test", test)
    print ("+++++Title", recipe_info["title"])
    #print (recipe_info['nutrition'])

    for item in recipe_info['nutrition']['nutrients']:
        name, amount, unit = (
            item["title"], 
            item["amount"], 
            item["unit"],)
        #print ("+++++name",name)
        #print ("+++++amount",amount)
        #print ("+++++unit", unit)
        if name=="Calories":
            cal_amount = amount
            print (cal_amount)

        if name=="Fat":
            fat = str(amount)+" "+unit
            print (fat)

        if name=="Protein":
            protein = str(amount)+" "+unit
            print (protein)

        if name=="Net Carbohydrates":
            carbs = str(amount)+" "+unit
            print (carbs)
    
    ingredients_list=[]

    for ingredient in recipe_info['nutrition']['ingredients']:
        #print(ingredient['name'], ingredient['amount'], ingredient['unit'])
        item=str(ingredient['amount']) + " " + ingredient['unit']+ " " + ingredient['name']      
        ingredients_list.append(item)
    
    #print("ingredients_list:", ingredients_list)

    instructions_list=[]
    
    for step in recipe_info['analyzedInstructions'][0]['steps']:
        #print(ingredient['name'], ingredient['amount'], ingredient['unit'])
        instructions_list.append(step['step'])
    

    summary = recipe_info['summary'].replace("</b>", "").replace("<b>", "")
    test = summary.split('.')
    # print("Summary", summary)

    # for i in test:
    #     print("i", i)

    #return render_template('recipe_details.html', recipe=recipe_details, summary=summary)
    return render_template('recipe_details.html', recipe=recipe_info, calories=cal_amount, fat=fat, protein=protein, carbs=carbs, ingredients_list=ingredients_list, summary=summary, instructions_list=instructions_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
