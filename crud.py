"""Functions for working with the database"""

import model

def add_new_user(fname, lname, email, password):
    user = model.User(fname=fname, lname=lname, email=email, password=password)
    model.db.session.add(user)
    model.db.session.commit()
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


if __name__ == "__main__":
    from server import app
    model.connect_to_db(app)