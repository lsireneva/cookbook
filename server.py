
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
import spoonacular as sp
import os
import json
from pprint import pformat
import requests
import model
import crud
import calendar
import datetime
from datetime import timedelta
import sendgrid_email_api


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
    if session.get('user_id') != None:
        user_id = session['user_id']
        fname = crud.get_user_fname(user_id)   
        return render_template('homepage.html', fname=fname)
    else:
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

    if crud.check_user_exist(email):
        flash('User account with this email already exist, Please login.', 'message')
        return redirect('/login')
    else:
        if crud.add_new_user(fname,lname,email,password):
            flash('New user account created', 'message')
            return redirect('/login')
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
    payload = {'ingredients': ingredients, 'number': 4, 'apiKey': API_KEY}

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
                'number': 4, 
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

    print ("+++++Title", recipe_info["title"])

    for item in recipe_info['nutrition']['nutrients']:
        print("item", item)
        name, amount, unit = (
            item["name"], 
            item["amount"], 
            item["unit"],)
       
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
        instructions_list.append(step['step'])
    
    return render_template('recipe_details.html', recipe=recipe_info, calories=cal_amount, fat=fat, protein=protein, carbs=carbs, ingredients_list=recipe_info["extendedIngredients"], instructions_list=instructions_list, recipe_id=recipe_id, dish_type=recipe_info["dishTypes"])


@app.route('/save_recipe_to_db', methods=['GET', 'POST'])
def save_recipe_to_db(): 
    recipe_info = request.get_json().get("recipe_info")
    
    #save to recipes table
    if not crud.check_record_exist("Recipe", recipe_info["title"]):
        crud.add_new_recipe(recipe_info["title"], recipe_info["instructions"], recipe_info["image"], recipe_info["time"], recipe_info["servings"], recipe_info["calories"], recipe_info["fat"], recipe_info["protein"], recipe_info["carbs"], recipe_info["notes"])
    elif not crud.check_in_favorites(crud.get_recipe_id(recipe_info["title"])):
        #save to favorites table
        if session.get("user_id"):
            print("USER_ID", session.get("user_id"))
            crud.add_new_favorite(session.get("user_id"), crud.get_recipe_id(recipe_info["title"]), recipe_info["dish_type"])
        return jsonify({"status": "Recipe saved to favorites"})
        
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
        print(ingredient["aisle"])
        if not crud.check_record_exist("Ingredient", ingredient["name"]):
            crud.add_new_ingredient(ingredient["name"], ingredient["image"], ingredient["aisle"])
    
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

@app.route('/recipe_details_db/<recipe_id>')
def get_recipe_details_db(recipe_id):

    print("FROM DB", recipe_id)
    
    recipe_details=crud.get_recipe_info(recipe_id)
    print("DB recipe name", recipe_details.recipe_name)
    print("DB recipe image", recipe_details.recipe_image)

    ingredients = crud.get_recipe_ingredients(recipe_id)
    print("INGREDIENTS:", ingredients)
    for i in ingredients:
     
        print("INGREDIENT_image:", i.ingredient_image)
        print("INGREDIENT_name:", i.ingredient_name)
        print("INGREDIENT_aisle:", i.ingredient_aisle)
        print("INGREDIENT_amount:", i.quantity)
        print("INGREDIENT_measure:", i.measure)
    
    instructions = recipe_details.recipe_instructions.strip().split("\n        \n        ")
    print("STEPS:", instructions)
    
    category = crud.get_recipe_category(recipe_id)

    print ("CATEGORY", category)

    return render_template('recipe_details_db.html', recipe=recipe_details, category=category, instructions=instructions, ingredients=ingredients)
    #return jsonify("You have already added this recipe to favorites")
@app.route('/import_recipe')
def import_recipe():

    return render_template('import_recipe.html')


@app.route('/imported_recipe', methods=['POST'])
def open_imported_recipe():

    recipe_link =request.form.get('recipe_link')
    print("LINK", recipe_link)

    url = f'https://api.spoonacular.com/recipes/extract?url={recipe_link}'
    payload = {'includeNutrition': True, 'apiKey': API_KEY}

    response = requests.get(url, params=payload)
    print ("response:", response)

    if response.status_code != 200:
        response.raise_for_status()
    
    recipe_info = response.json()

    print ("+++++Title", recipe_info["title"])

    for item in recipe_info['nutrition']['nutrients']:
        name, amount, unit = (
            item["name"], 
            item["amount"], 
            item["unit"],)
      
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

        instructions_list=[]
        for step in recipe_info['analyzedInstructions'][0]['steps']:
            instructions_list.append(step['step'])

    return render_template('recipe_details.html', recipe=recipe_info, calories=cal_amount, fat=fat, protein=protein, carbs=carbs, ingredients_list=recipe_info["extendedIngredients"], instructions_list=instructions_list, dish_type=recipe_info["dishTypes"])

@app.route('/delete_recipe_db', methods=['GET', 'POST'])
def delete_recipe_db(): 
    recipe_name = request.get_json().get("recipe_name")
    print("DELETE", recipe_name)  
    crud.delete_recipe_favorite(recipe_name)
    
    return jsonify({"status": "Recipe deleted from favorites"})

@app.route('/delete_recipe_from_mealplan', methods=['POST'])
def delete_recipe_from_mealplan():
    recipe_name = request.get_json().get("recipe_name")
    print("DELETE FROM MEAL PLAN", recipe_name)
    crud.delete_recipe_meal_plan(recipe_name)

    return jsonify({"status": "Recipe deleted from meal plan"})

@app.route('/save_to_meal_plan', methods=['GET', 'POST'])
def save_to_meal_plan():
    recipe_info = request.get_json().get("recipe_info")
    print(recipe_info)
    #save to recipes table
    if not crud.check_record_exist("Recipe", recipe_info["title"]):
        crud.add_new_recipe(recipe_info["title"], recipe_info["instructions"], recipe_info["image"], recipe_info["time"], recipe_info["servings"], recipe_info["calories"], recipe_info["fat"], recipe_info["protein"], recipe_info["carbs"], recipe_info["notes"])

    #save to meal_plans table
    if session.get("user_id"):
        print("USER_ID", session.get("user_id"))
        crud.add_new_meal_plan(session.get("user_id"), crud.get_recipe_id(recipe_info["title"]), recipe_info["meal_category"], recipe_info["meal_date"])
    
    #save to ingredients table and to IngredientToRecipe table
    for ingredient in recipe_info["ingredients"]:
        print(ingredient["name"])
        print(ingredient["image"])
        print(ingredient["aisle"])
        if not crud.check_record_exist("Ingredient", ingredient["name"]):
            crud.add_new_ingredient(ingredient["name"], ingredient["image"], ingredient["aisle"])
    
    for ingredient in recipe_info["ingredients"]:
        print(ingredient["amount"])
        print(ingredient["unit"])
        print(crud.get_ingredient_id(ingredient["name"]))

        if crud.get_recipe_id(recipe_info["title"]) is not None:
            if not crud.check_record_in_ingredients_to_recipes(crud.get_recipe_id(recipe_info["title"]), crud.get_ingredient_id(ingredient["name"])):
                crud.add_ingredient_to_recipe(crud.get_recipe_id(recipe_info["title"]), crud.get_ingredient_id(ingredient["name"]), ingredient["amount"], ingredient["unit"])
    
    
    return jsonify({"status": "Recipe added to meal plan"})


@app.route('/show_meal_plan')
def show_meal_plan():
    current_time = datetime.date.today()
    print("CURRENT TIME", current_time)
    year, week_num, day_of_week = current_time.isocalendar()
    print("Week #" + str(week_num) + " of year " + str(year))

    monday = datetime.datetime.strptime(f'{str(year)}-{str(week_num)}-1', "%Y-%W-%w").date()
    sunday = monday + datetime.timedelta(days=6.9)
    
    
    meal_plan = crud.get_all_meal_plan_current_week(session.get("user_id"), monday, sunday)
    #print("+++++++MEAL_PLAN", meal_plan)

    meal_plan_arr=[]
    meal_dict={}
    for meal in meal_plan:
        print("+++++++MEAL PLAN", meal)

        meal_info=crud.get_mealplan_recipe_info(meal.recipe_id)
        print("+++++++MEAL INFO", meal_info)

        if meal_info.date not in meal_dict:
            meal_dict[meal_info.date]={"breakfast": [], "lunch": [], "dinner": []}
        
        meal_dict[meal_info.date][meal_info.category].append(meal)
        

    meal_plan_arr.append(meal_dict)
    print("MEAL DICTIONARY", meal_dict)
    print("ARRAY MEAL PLAN ALL", meal_plan_arr)
    
    return render_template('meal_calendar.html', meal_plan=meal_plan_arr, start_day=monday, end_day=sunday)

@app.route('/open_meal_plan', methods=['GET', 'POST'])
def open_meal_plan():
    print("inside of route open_meal_plan")
   
    monday = request.form.get('monday')
    sunday = request.form.get('sunday')
    print("monday", monday)
    print("sunday", sunday)

    meal_plan = crud.get_all_meal_plan_current_week(session.get("user_id"), monday, sunday)
    print("+++++++MEAL_PLAN", meal_plan)
    
    meal_plan_arr=[]
    meal_dict={}
    for meal in meal_plan:
        print("+++++++MEAL PLAN", meal)

        meal_info=crud.get_mealplan_recipe_info(meal.recipe_id)
        print("+++++++MEAL INFO", meal_info)

        if meal_info.date not in meal_dict:
            meal_dict[meal_info.date]={"breakfast": [], "lunch": [], "dinner": []}
        
        meal_dict[meal_info.date][meal_info.category].append(meal)
        

    meal_plan_arr.append(meal_dict)
    print("MEAL DICTIONARY", meal_dict)
    print("ARRAY MEAL PLAN ALL", meal_plan_arr)

    return render_template('meal_calendar.html', meal_plan=meal_plan_arr, start_day=monday, end_day=sunday)

@app.route('/open_recipe_meal_plan/<recipe_name>', methods=['GET', 'POST'])
def open_recipe_meal_plan(recipe_name):
    print("OPEN RECIPE MEAL PLAN")
    print("OPEN recipe_name",recipe_name)
    recipe_id = crud.get_recipe_id(recipe_name)
    
    return redirect(url_for('.get_recipe_details_db', recipe_id = recipe_id))
   
@app.route('/get_grocery_list/<start_day>/<end_day>', methods=['GET', 'POST'])
def get_grocery_list(start_day, end_day):
    grocery_list = crud.get_all_meal_plan_current_week(session.get("user_id"), start_day, end_day)
    print("GROCERY LIST", grocery_list)
    
    all_ingredients={}
    for item in grocery_list:
        print (item.recipe_name)
        ingredients = crud.get_recipe_ingredients(item.recipe_id)
        for i in ingredients:
            print("+++++ingredient", i)
            if i.ingredient_aisle not in all_ingredients:
                all_ingredients[i.ingredient_aisle]=set()
            all_ingredients[i.ingredient_aisle].add(i.ingredient_name)

    print ("____all_ingredients:", all_ingredients)
    
    if all_ingredients:
        return render_template('grocery_list.html', grocery_list=all_ingredients, start_day=start_day, end_day=end_day)
    else:
        flash("There is no meal plan for this week")
        return redirect("/show_meal_plan")

@app.route('/send_email', methods=['POST'])
def send_email_by_sendgrid():
    grocery_list_info = request.get_json().get("grocery_list_info")
    grlist = grocery_list_info['grocery_list']
    html_content = f"<h1>Grocery list for a week {grocery_list_info['start_day']} - {grocery_list_info['end_day']}:</h1><ol>"
    
    for item in grlist:
        print(item)
        print(grlist[item])
        html_content += f"<h2>{item}</h2><ul>"
        for i in grlist[item]:
            print(i)        
            html_content += f"<li>{i}</li>"
        html_content +="</ul>"
    print(html_content)
    sendgrid_email_api.send_email(grocery_list_info['email'], "subject: grocery list", html_content)
    
    return jsonify({"status": "Email sent"})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

