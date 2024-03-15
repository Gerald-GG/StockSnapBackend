from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize SQLAlchemy database
db = SQLAlchemy()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Import models here to avoid circular imports
from .stock import StockResource  # Import the StockResource from models.stock
