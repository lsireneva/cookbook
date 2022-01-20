"""Functions for working with the database"""

import model

def add_to_db(record):
    model.db.session.add(record)
    model.db.session.commit()

def add_new_user(fname, lname, email, password):
    user = model.User(fname=fname, lname=lname, email=email, password=password)
    add_to_db(user)
    return True

def add_new_recipe(recipe_name, recipe_instructions, recipe_image, time, servings, calories, fat, protein, carbs, note):
    recipe = model.Recipe(recipe_name=recipe_name, recipe_instructions=recipe_instructions, recipe_image=recipe_image, time=time, servings=servings, calories=calories, fat=fat, protein=protein, carbs=carbs, note=note)
    add_to_db(recipe)
    return True


def add_new_favorite(user_id, recipe_id, category):
    favorite = model.Favorite(user_id=user_id, recipe_id=recipe_id, category=category)
    add_to_db(favorite)
    return True

def add_new_ingredient(name, image):
    ingredient = model.Ingredient (ingredient_name=name, ingredient_image=image)
    add_to_db(ingredient)
    return True

def add_ingredient_to_recipe(recipe_id, ingredient_id, quantity, measure):
    ingredient_to_recipe = model.IngredientToRecipe(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity, measure=measure)
    add_to_db(ingredient_to_recipe)
    return True

def check_login(email, password):
    user = model.User.query.filter(model.User.email == email).one()
    print ("CRUD USER", user)
    
    if user.email != email or user.password != password:
        return False
    return user

def get_user_fname(user_id):
    user = model.User.query.filter(model.User.user_id==user_id).one()
    
    return user.fname

def get_recipe_id(name):
    recipe = model.Recipe.query.filter(model.Recipe.recipe_name==name).one()

    return recipe.recipe_id

def get_ingredient_id(name):
    ingredient = model.Ingredient.query.filter(model.Ingredient.ingredient_name==name).one()
    print ("CRUD GET INGREDIENT ID", ingredient.ingredient_id)
    return ingredient.ingredient_id

if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)