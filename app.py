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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Detect if running on Render
is_render = "render.com" in DATABASE_URL

# Import additional config parameters for database
import os

# Get database pool configuration from environment
pool_size = int(os.environ.get("SQLALCHEMY_POOL_SIZE", "5"))
max_overflow = int(os.environ.get("SQLALCHEMY_MAX_OVERFLOW", "10"))
pool_timeout = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", "30"))
pool_recycle = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", "300"))

# Enhanced SQL engine options for production stability
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    # Connection pool settings from environment or defaults
    "pool_recycle": pool_recycle,  # Recycle connections after this many seconds
    "pool_pre_ping": True,        # Test connections before using them
    "pool_timeout": pool_timeout,  # Seconds to wait for a connection from pool
    "pool_size": pool_size,       # Maximum number of persistent connections
    "max_overflow": max_overflow, # Maximum number of connections above pool_size
    
    # Set connection arguments for SSL if on Render
    "connect_args": {
        # Use SSL based on environment variable with fallback based on host
        "sslmode": os.environ.get("SSL_MODE", "require" if is_render else "prefer"),
        
        # Connection retry settings
        "connect_timeout": 10,
        
        # Keep-alive settings to maintain connections
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
        
        # Enhanced SSL options for Render
        "ssl_cert_reqs": "CERT_NONE" if os.environ.get("SSL_CERT_REQS_NONE", "false").lower() == "true" else None
    }
}

# Log database configuration
logger.info(f"Database URL: {'PostgreSQL database' if 'postgres' in DATABASE_URL else DATABASE_URL}")
logger.info(f"SSL Mode: {os.environ.get('SSL_MODE', 'require' if is_render else 'prefer')}")
logger.info(f"Pool size: {pool_size}, Max overflow: {max_overflow}, Timeout: {pool_timeout}s, Recycle: {pool_recycle}s")
logger.info(f"Max DB Retries: {os.environ.get('DB_MAX_RETRIES', '3')}, Retry Delay: {os.environ.get('DB_RETRY_DELAY', '0.5')}s")

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