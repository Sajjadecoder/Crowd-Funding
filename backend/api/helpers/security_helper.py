import jwt
import datetime
from functools import wraps
from flask import current_app, request, jsonify

def generate_jwt(user_id, role):
    payload = {
        "role": role,
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            user_id = verify_jwt(token)
            return f(user_id=user_id, *args, **kwargs)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_login import current_user
            if getattr(current_user, 'is_authenticated', False) and str(getattr(current_user, 'role', '')).lower() == 'admin':
                return f(*args, **kwargs)
        except Exception:
            pass

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if payload.get("role") != "admin":
                return jsonify({"error": "Admins only"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return decorated_function

def creator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_login import current_user
            if getattr(current_user, 'is_authenticated', False) and str(getattr(current_user, 'role', '')).lower() == 'creator':
                return f(*args, **kwargs)
        except Exception:
            pass

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if payload.get("role") != "creator":
                return jsonify({"error": "Creators only"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return decorated_function