from flask import jsonify, request, current_app, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db  # Import the db object from models
from werkzeug.security import generate_password_hash, check_password_hash  # Import password hashing functions
import logging
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# User Registration Resource
class UserRegistrationResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not password or not email:
                return {"error": "Username, password, and email are required."}, 400

            # Check email format
            if not "@" in email or not "." in email:
                return {"error": "Invalid email format."}, 400

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"error": "Email is already taken."}, 400

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new user instance
            new_user = User(username=username, email=email, password=hashed_password)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            return {"message": "User registered successfully."}, 201
        except Exception as e:
            return {"error": "Failed to register user. Please try again later."}, 500

# User Login Resource
class UserLoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {"error": "Email and password are required."}, 400

            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.email)  # Use email as identity
                return {"access_token": access_token}, 200
            else:
                return {"error": "Invalid email or password."}, 401
        except Exception as e:
            # Log the exception for debugging
            logging.exception("An error occurred during login:")
            return {"error": "Failed to log in. Please try again later."}, 500

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {"access_token": access_token}, 200
        except Exception as e:
            return {"error": "Failed to refresh access token."}, 500

# User Resource (Get user information)
class UserResource(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }, 200
            else:
                return {"message": "User not found."}, 404
        except Exception as e:
            return {"error": "Failed to retrieve user information."}, 500

    @jwt_required()
    def put(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if not user:
                return {"message": "User not found."}, 404

            # Check if the request contains a file
            if 'image' not in request.files:
                return {"error": "No file provided."}, 400

            # Get the file from the request
            image = request.files['image']

            # Save the image
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                return {"message": "Image uploaded successfully."}, 200
            else:
                return {"error": "Invalid image file."}, 400
        except BadRequest:
            return {"error": "Invalid image file."}, 400
        except Exception as e:
            return {"error": "Failed to upload image."}, 500

    @jwt_required()
    def delete(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()

            if not user:
                return {"message": "User not found."}, 404

            # Delete the user's image file
            if user.image_url:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], user.image_url))
                user.image_url = None
                db.session.commit()
                return {"message": "Image deleted successfully."}, 200
            else:
                return {"message": "No image to delete."}, 404
        except Exception as e:
            return {"error": "Failed to delete image."}, 500

# Serve User Images
class ServeImage(Resource):
    def get(self, filename):
        try:
            return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
        except FileNotFoundError:
            return {"error": "Image not found."}, 404

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
