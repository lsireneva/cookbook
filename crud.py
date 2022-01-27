"""Functions for working with the database"""
from model import User, Recipe, Ingredient, IngredientToRecipe, Favorite, MealPlan, connect_to_db, db

def add_to_db(record):
    db.session.add(record)
    db.session.commit()

def add_new_user(fname, lname, email, password):
    user = User(fname=fname, lname=lname, email=email, password=password)
    add_to_db(user)
    return True

def add_new_recipe(recipe_name, recipe_instructions, recipe_image, time, servings, calories, fat, protein, carbs, note):
    recipe = Recipe(recipe_name=recipe_name, recipe_instructions=recipe_instructions, recipe_image=recipe_image, time=time, servings=servings, calories=calories, fat=fat, protein=protein, carbs=carbs, note=note)
    add_to_db(recipe)
    return True


def add_new_favorite(user_id, recipe_id, category):
    favorite = Favorite(user_id=user_id, recipe_id=recipe_id, category=category)
    add_to_db(favorite)
    return True

def add_new_meal_plan(user_id, recipe_id, meal_category, meal_date):
    meal_plan = MealPlan(user_id=user_id, recipe_id=recipe_id, category=meal_category, date=meal_date)
    add_to_db(meal_plan)
    return True

def add_new_ingredient(name, image):
    ingredient = Ingredient(ingredient_name=name, ingredient_image=image)
    add_to_db(ingredient)
    return True

def add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, measure):
    ingredient_to_recipe = IngredientToRecipe(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity, measure=measure)
    add_to_db(ingredient_to_recipe)
    return True

def check_user_exist(email):
    email=User.query.filter(User.email == email).first()
    
    if email is not None:
        return True
    
    return False

def check_login(email, password):
    user = User.query.filter(User.email == email).first()
    print ("CRUD USER", user)
    
    if user.email != email or user.password != password:
        return False
    return user

def check_record_exist(table, name):
    print("CRUD table:", table)
    print("CRUD name:", name)
    if table=="Recipe":
        record = Recipe.query.filter(Recipe.recipe_name == name).first()
        if record is not None:
            print ("CRUD Recipe already exist")
            return True
    elif table=="Ingredient":
        record = Ingredient.query.filter(Ingredient.ingredient_name == name).first()
        if record is not None:
            print ("CRUD Ingredient alredy exist")
            return True
    else:
        return False

def check_in_favorites(recipe_id):
    fav_recipe = Favorite.query.filter(Favorite.recipe_id==recipe_id).first()
    if fav_recipe is not None:
        return True
    return False

def get_user_fname(user_id):
    user = User.query.filter(User.user_id==user_id).first()
    if user is not None:
        return user.fname
    

def get_recipe_id(name):
    recipe = Recipe.query.filter(Recipe.recipe_name==name).first()

    print("CRUD recipe_id=", recipe.recipe_id)
    return recipe.recipe_id

def get_recipe_info(recipe_id):
    recipe = Recipe.query.filter(Recipe.recipe_id==recipe_id).first()

    return recipe

def get_ingredient_id(name):
    ingredient = Ingredient.query.filter(Ingredient.ingredient_name==name).first()
    print ("CRUD GET INGREDIENT ID", ingredient.ingredient_id)
    return ingredient.ingredient_id

def get_all_favorites(user_id):
    favorites=db.session.query(Recipe).join(Favorite).filter(Favorite.user_id==user_id).all()
    return favorites

def get_all_meal_plan(user_id):
    meal_plan=db.session.query(Recipe).join(MealPlan).filter(MealPlan.user_id==user_id).order_by(MealPlan.date, MealPlan.category).all()
    return meal_plan

def get_mealplan_info(recipe_id):
    mealplan_info=MealPlan.query.filter(MealPlan.recipe_id==recipe_id).first()
    return mealplan_info

def get_recipe_category(recipe_id):
    favorite = Favorite.query.filter(Favorite.recipe_id==recipe_id).first()
    return favorite.category

def get_recipe_ingredients(recipe_id):
    ingredients = db.session.query(Ingredient.ingredient_name, Ingredient.ingredient_image,
                        IngredientToRecipe.quantity, IngredientToRecipe.measure).join(IngredientToRecipe).filter(IngredientToRecipe.recipe_id==recipe_id).all()

    return ingredients

def get_ingredient_amount_measure(recipe_id):
    amount_measure=IngredientToRecipe.query.filter(IngredientToRecipe.recipe_id==recipe_id).all()
    return amount_measure

def delete_recipe(recipe_name):
    recipe_id = get_recipe_id(recipe_name)
    print("CRUD DELETE RECIPE", recipe_id)
    delete_recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).first()
    delete_favorite=Favorite.query.filter(Favorite.recipe_id == recipe_id).first()
    delete_ingredienttorecipe=IngredientToRecipe.query.filter(IngredientToRecipe.recipe_id == recipe_id).all()
    db.session.delete(delete_recipe)
    db.session.delete(delete_favorite)
    for i in delete_ingredienttorecipe:
        db.session.delete(i)
    db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)