from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize SQLAlchemy database without associating it with the Flask app yet
db = SQLAlchemy()

# Initialize Flask application
app = Flask(__name__)

# Configure the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocksnap.db'  # SQLite database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
app.config['SECRET_KEY'] = '8a3339628ed6875e08574ab2afcec3e770033cd316cbfad6'  # Secret key for session management (replace with a long random string)

# Enable CORS
CORS(app)

# Associate SQLAlchemy database with the Flask app using init_app method
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import routes after initializing db to avoid circular imports
from routes.auth import auth_routes
from routes.stocks import stocks_routes

# Register routes
app.register_blueprint(auth_routes)
app.register_blueprint(stocks_routes)

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)  # Set debug=True for development
