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
recipe1 = Recipe(recipe_name="Macaroni and cheese", recipe_directions="Cook macaroni according to the package directions. Drain.", recipe_image="some link", note="Sprinkle with a little paprika.")

db.session.add(user1)
db.session.add(recipe1)

db.session.commit()