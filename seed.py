import os
import datetime
from model import User, Recipe, connect_to_db, db
from server import app

os.system("dropdb cookbook")
os.system("createdb cookbook")

connect_to_db(app)
db.create_all()
    

user = User(id=1, fname="Luba", lname="Developer", email="luba@test.test", password="123")
recipe = Recipe(recipe_id=1, recipe_name="Macaroni and cheese", recipe_directions="Cook macaroni according to the package directions. Drain.", recipe_image="some link", note="Sprinkle with a little paprika.")

db.session.add(user)
db.session.add(recipe)
