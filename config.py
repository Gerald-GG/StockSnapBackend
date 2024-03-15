import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management (replace with a long random string)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'stocksnap.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS settings
    CORS_HEADERS = 'Content-Type'
