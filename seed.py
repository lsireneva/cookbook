import os
import datetime
from model import User, Recipe, connect_to_db, db
from server import app

os.system("dropdb cookbook")
os.system("createdb cookbook")


connect_to_db(app)
db.drop_all()
db.create_all()
    

user1 = User(fname="Luba", lname="Developer", email="luba@test.com", password="123")
recipe1 = Recipe(recipe_name="Chicken Stew", recipe_instructions="Slice the onions.", recipe_image="link", time="45 min", servings="6", calories="330", fat="20 g", protein="17 g", carbs="15 g", note="add garlic")

db.session.add(user1)
db.session.add(recipe1)

db.session.commit()