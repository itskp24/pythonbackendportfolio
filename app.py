"""
Main application configuration file that initializes Flask app and database
"""
import os
import logging
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logger = logging.getLogger(__name__)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Create the Flask application
app = Flask(__name__)

# Configure the application
from config import DATABASE_URL, SECRET_KEY

# Configure app secret key
app.secret_key = SECRET_KEY

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create all database tables
with app.app_context():
    try:
        # Import models to ensure they are registered with SQLAlchemy
        from models import Contact
        
        # Create tables
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

# Import and register routes
from routes.contact_routes import contact_bp
from routes.health_routes import health_bp

app.register_blueprint(contact_bp)
app.register_blueprint(health_bp)

# Add error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def server_error(error):
    return {"error": "Internal server error"}, 500