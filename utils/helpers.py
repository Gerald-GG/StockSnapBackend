from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, bcrypt

# Function to generate access token for user
def generate_access_token(user):
    return create_access_token(identity=user.email)

# Function to check if the user is authenticated
def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

# Function to get the current user
def get_current_user():
    email = get_jwt_identity()
    return User.query.filter_by(email=email).first()

# Function to validate email format
def is_valid_email(email):
    return '@' in email and '.' in email

# Function to validate password strength
def is_strong_password(password):
    # Add your password strength criteria here
    return len(password) >= 8

# Function to validate if a field is not empty
def is_not_empty(value):
    return value.strip() != ''
