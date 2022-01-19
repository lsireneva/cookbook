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

def check_login (email, password):

    user = model.User.query.filter(model.User.email == email).one()
    print ("CRUD USER", user)
    
    if user.email != email or user.password != password:
        return False

    return user

def get_user_fname(user_id):

    user = model.User.query.filter(model.User.user_id==user_id).one()
    
    return user.fname


def save_favorites(name, instructions, image, note):

    return True


if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)