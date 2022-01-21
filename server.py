
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
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

# Load recipe data from JSON file
#with open("data/recipe_information.json") as f:
#    recipe_info = json.loads(f.read())

@app.route('/')
def homepage():
    """Show homepage."""
    print("GET SESSION:",session.get('user_id'))
    if session.get('user_id') == None:
        return render_template('homepage.html')
    else:
        user_id = session['user_id']
        fname = crud.get_user_fname(user_id)   
        return render_template('homepage.html', fname=fname)
        

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
        flash('New user account created', 'message')
    else:
        flash('User creation failed', 'error')
    return redirect('/')


@app.route('/login')
def login():
    """User login page"""

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User log out"""
    if session.get("user_id"):
        session.clear()
        flash("User logged out.")
    
    return redirect("/")

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
        flash('You were successfully logged in')
        return redirect(url_for('.homepage', user_id = user.user_id))
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
    #print ("response:", response)

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
    #print (recipe_info)

    print ("+++++Title", recipe_info["title"])

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
    
    # get ingredients
    # ingredients_list=[]

    # for ingredient in recipe_info['nutrition']['ingredients']:
    #     #print(ingredient['name'], ingredient['amount'], ingredient['unit'])
    #     item=str(ingredient['amount']) + " " + ingredient['unit']+ " " + ingredient['name']      
    #     ingredients_list.append(item)
    
    #print("ingredients_list:", ingredients_list)
    
    #get instructions
    instructions_list=[]
    for step in recipe_info['analyzedInstructions'][0]['steps']:
        #print(ingredient['name'], ingredient['amount'], ingredient['unit'])
        instructions_list.append(step['step'])
    
    # for ingredient in recipe_info["extendedIngredients"]:
    #     print(ingredient["name"])
    #     print(ingredient["amount"])
    #     print(ingredient["unit"])
    #     print(ingredient["image"])
    
    return render_template('recipe_details.html', recipe=recipe_info, calories=cal_amount, fat=fat, protein=protein, carbs=carbs, ingredients_list=recipe_info["extendedIngredients"], instructions_list=instructions_list, recipe_id=recipe_id, dish_type=recipe_info["dishTypes"])


@app.route('/save_recipe_to_db', methods=['GET', 'POST'])
def save_recipe_to_db(): 
    recipe_info = request.get_json().get("recipe_info")
    #print (recipe_info)
    #save to recipes table
    if not crud.check_record_exist("Recipe", recipe_info["title"]):
        crud.add_new_recipe(recipe_info["title"], recipe_info["instructions"], recipe_info["image"], recipe_info["time"], recipe_info["servings"], recipe_info["calories"], recipe_info["fat"], recipe_info["protein"], recipe_info["carbs"], recipe_info["notes"])
    else:
        return jsonify({"status": "You have already added this recipe to favorites"})

    #save to favorites table
    if session.get("user_id"):
        print("USER_ID", session.get("user_id"))
        crud.add_new_favorite(session.get("user_id"), crud.get_recipe_id(recipe_info["title"]), recipe_info["dish_type"])
    
    #save to ingredients table and to IngredientToRecipe table
    for ingredient in recipe_info["ingredients"]:
        print(ingredient["name"])
        print(ingredient["image"])
        if not crud.check_record_exist("Ingredient", ingredient["name"]):
            crud.add_new_ingredient(ingredient["name"], ingredient["image"])
    
    for ingredient in recipe_info["ingredients"]:
        print(ingredient["amount"])
        print(ingredient["unit"])
        print(crud.get_ingredient_id(ingredient["name"]))
        
        if crud.get_recipe_id(recipe_info["title"]) is not None:
            crud.add_ingredient_to_recipe(crud.get_recipe_id(recipe_info["title"]), crud.get_ingredient_id(ingredient["name"]), ingredient["amount"], ingredient["unit"])
    
    
    return jsonify({"status": "Recipe saved to favorites"})

@app.route('/favorites', methods=['GET', 'POST'])
def open_favorites():
    
    favorites = crud.get_all_favorites(session.get("user_id"))
    print("+++++++FAVORITES", favorites)

    for fav in favorites:
        print("+++++++FAV", fav)
        print(fav.recipe_name)

    return render_template('favorites.html', favorites=favorites)

@app.route('/recipe_details_db/<recipe_id>', methods=['POST'])
def get_recipe_details_db(recipe_id):


    #return render_template('recipe_details.html')
    return f"recipe details for {recipe_id}"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
