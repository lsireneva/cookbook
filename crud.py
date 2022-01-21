"""Functions for working with the database"""

from model import User, Recipe, Ingredient, IngredientToRecipe, Favorite, connect_to_db, db

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

def add_new_ingredient(name, image):
    ingredient = Ingredient(ingredient_name=name, ingredient_image=image)
    add_to_db(ingredient)
    return True

def add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, measure):
    ingredient_to_recipe = IngredientToRecipe(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity, measure=measure)
    add_to_db(ingredient_to_recipe)
    return True

def check_login(email, password):
    user = User.query.filter(User.email == email).one()
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


def get_user_fname(user_id):
    user = User.query.filter(User.user_id==user_id).one()
    
    return user.fname

def get_recipe_id(name):
    recipe = Recipe.query.filter(Recipe.recipe_name==name).first()

    print("CRUD recipe_id=", recipe.recipe_id)
    return recipe.recipe_id

def get_ingredient_id(name):
    ingredient = Ingredient.query.filter(Ingredient.ingredient_name==name).one()
    print ("CRUD GET INGREDIENT ID", ingredient.ingredient_id)
    return ingredient.ingredient_id

def get_all_favorites(user_id):
    favorites = Recipe.query.options(db.joinedload("favorites")).filter(Favorite.user_id==user_id).all()
    return favorites

if __name__ == "__main__":
    from server import app
    connect_to_db(app)