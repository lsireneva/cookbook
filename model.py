"""Models for cookbook app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    
    """Users in cook book app"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String)

    favorites = db.relationship('Favorite', backref='user')
    meal_plan = db.relationship('MealPlan', backref='user')

    # user object
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Recipe(db.Model):

    """Saved recipes by user"""

    __tablename__= "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_name = db.Column(db.String, unique=True, nullable=False)
    recipe_instructions = db.Column(db.String, nullable=False)
    recipe_image = db.Column(db.String)
    time = db.Column(db.String(25))
    servings = db.Column(db.String(25))
    calories = db.Column(db.String(25))
    fat = db.Column(db.String(25))
    protein = db.Column(db.String(25))
    carbs = db.Column(db.String(25))
    note = db.Column(db.String(300))

    favorites = db.relationship('Favorite', backref='recipe')
    meal_plan=db.relationship('MealPlan', backref='recipe')
    ingredients_to_recipes = db.relationship('IngredientToRecipe', backref='recipe')

    # recipe object
    def __repr__(self):
        return f"<Recipe recipe_id={self.recipe_id} recipe_name={self.recipe_name} recipe_image={self.recipe_image} time={self.time}>"


class Ingredient(db.Model):
    
    """Ingredient for recipe"""

    __tablename__="ingredients"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_name = db.Column(db.String(50), unique=True, nullable=False)
    ingredient_image = db.Column(db.String(100), nullable=False)
    ingredient_aisle=db.Column(db.String)

    ingredients_to_recipes = db.relationship('IngredientToRecipe', backref='ingredient')

    # ingredient object
    def __repr__(self):
        return f"<Ingredient ingredient_id={self.ingredient_id} name={self.ingredient_name} image={self.ingredient_image}>"


class IngredientToRecipe(db.Model):
    """Ingredients list for recipe"""

    __tablename__="ingredients_to_recipes"

    ingredients_to_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    measure = db.Column(db.String(25), nullable=False)

    # ingredients_to_recipes (db.relationship('IngredientToRecipe', backref='ingredient') on Ingredient model)
    # ingredients_to_recipes (db.relationship('IngredientToRecipe', backref='recipe') on Recipe model)

    # ingredient_to_recipe object
    def __repr__(self):
        return f"<Ingredient_to_recipe recipe_id={self.recipe_id} ingredient_id={self.ingredient_id} quantity={self.quantity} measure={self.measure}>"


class Favorite(db.Model):
    """Favorite recipes""" 

    __tablename__="favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    # user (db.relationship('Favorite', backref='user') on User model)
    # recipe (db.relationship('Favorite', backref='recipe') on Recipe model)

    # favorite object
    def __repr__(self):
        return f"<Favorite favorite_id={self.favorite_id} category={self.category}>"

class MealPlan(db.Model):
    """Recipes for a meal plan""" 

    __tablename__="meal_plans"

    meal_plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # user (db.relationship('MealPlan', backref='user') on User model)
    # recipe (db.relationship('MealPlan', backref='recipe') on Recipe model)

    # meal plan object
    def __repr__(self):
        return f"<MealPlan meal_plan_id={self.meal_plan_id} category={self.category} date={self.date}>"




def connect_to_db(flask_app, db_uri="postgresql:///cookbook", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

