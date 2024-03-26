from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError  # Import IntegrityError for database integrity violations
import logging  # Import logging for logging errors
from models import db, bcrypt
from models.user import User  # Import the User model

auth_routes = Blueprint('auth_routes', __name__)

# User Registration Endpoint
@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not password or not email:
            return jsonify({"error": "Username, password, and email are required."}), 400

        # Check email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format."}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email is already taken."}), 400

        # Additional password validation (e.g., minimum length)
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long."}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully."}), 201
    except IntegrityError:
        # Handle database integrity violations (e.g., duplicate email)
        db.session.rollback()  # Rollback transaction
        return jsonify({"error": "Email is already taken."}), 400
    except Exception as e:
        # Log the error for debugging
        logging.error(f"Failed to register user: {str(e)}")
        return jsonify({"error": "Failed to register user. Please try again later."}), 500
