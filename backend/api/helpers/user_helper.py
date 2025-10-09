from api import db, bcrypt
from api.models.cf_models import Users, UserRole
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_user(username, password, email, role=None, profile_image=None):
    user_args = {"username": username, "email": email, "profile_image": profile_image}

    if role:
        # Accept either a UserRole or a string role
        user_args["role"] = role if isinstance(role, UserRole) else UserRole(role)

    user = Users(**user_args)
    user.setPasswordHash(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("User with username or email already exists.")
    except Exception as e:
        raise RuntimeError(f"Could not create a new user:{str(e)}")

    return user.to_dict()

def change_password(user_id, new_password):
    user = Users.query.get(user_id)
    if not user:
        raise ValueError("User not found.")

    user.setPasswordHash(new_password)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not change the password: {str(e)}")

    return {"message": "Password updated successfully", "user_id": user.user_id}

def search_users(keyword):
    users = Users.query.filter(
        (Users.username.ilike(f"%{keyword}%")) | (Users.email.ilike(f"%{keyword}%"))
    ).all()
    return [u.to_dict() for u in users]

def update_user(user_id, **kwargs):
    user = Users.query.get(user_id)
    if not user:
        raise ValueError("User not found.")

    allowed_fields = ["email", "username", "role", "profile_image"]
    for field, value in kwargs.items():
        if field in allowed_fields:
            if field == "role":
                user.role = value if isinstance(value, UserRole) else UserRole(value)
            else:
                setattr(user, field, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("User with email or username already exists.")
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not update the user: {str(e)}")

    return user.to_dict()


def checkLoginCredentials(identifier, password):
    user = Users.query.filter((Users.username == identifier) | (Users.email == identifier)).first()

    if not user:
        raise ValueError("Incorrect username/email or password")

    if not user.checkHashedPassword(password):
        raise ValueError("Incorrect username/email or password")

    return user.to_dict()

def get_all_users():
    users = Users.query.all()
    rows = [u.to_dict() for u in users]
    return rows


def get_user_by_username(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return None
    return user.to_dict()


def get_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    if not user:
        return None
    return user.to_dict()


def view_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise ValueError("User not found.")
    return user.to_dict()


def delete_user(user_id):
    user = Users.query.get(user_id)

    if not user:
        raise ValueError("No user found.")

    try:
        db.session.delete(user)
        db.session.commit()
        return {"Deleted user id": user_id}
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not delete user with id {user_id}: {str(e)}")


def delete_all_users():
    try:
        deleted = db.session.query(Users).delete()
        db.session.commit()
        return {"message": f"Successfully deleted {deleted} users"}
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Could not delete all users: {str(e)}")