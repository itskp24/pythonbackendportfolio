"""
Configuration module for the application
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# API configuration
API_PREFIX = '/api/v1'
API_PORT = int(os.environ.get('API_PORT', 5000))

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

# Flask configuration
DEBUG = os.environ.get('FLASK_ENV') == 'development'
SECRET_KEY = os.environ.get('SESSION_SECRET', 'default-secret-key-for-development')