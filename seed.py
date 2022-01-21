import os
import datetime
from model import User, Recipe, Favorite, connect_to_db, db
from server import app

os.system("dropdb cookbook")
os.system("createdb cookbook")


connect_to_db(app)
db.create_all()
    

user1 = User(fname="Luba", lname="Developer", email="luba@test.com", password="123")
recipe1 = Recipe(recipe_name="Chicken Stew", recipe_instructions="Slice the onions.", recipe_image="https://spoonacular.com/recipeImages/638343-556x370.jpg", time="45 min", servings="6", calories="330", fat="20 g", protein="17 g", carbs="15 g", note="add garlic")
favorite1= Favorite(user_id = 1, recipe_id = 1, category = "lunch")

db.session.add(user1)
db.session.add(recipe1)
db.session.add(favorite1)

db.session.commit()