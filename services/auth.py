"""
Authentication service for the API
"""
import logging
from flask_httpauth import HTTPBasicAuth
from flask import jsonify

logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()

# For simplicity, using static credentials in this demo
# In a production environment, this should be replaced with a proper user auth system
ADMIN_USERNAME = "kp"
ADMIN_PASSWORD = "kp@123"

@auth.verify_password
def verify_password(username, password):
    """
    Verify username and password for basic authentication
    """
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        logger.info(f"Authentication successful for user: {username}")
        return username
    logger.warning(f"Authentication failed for user: {username}")
    return None

@auth.error_handler
def auth_error():
    """
    Handle authentication errors
    """
    return jsonify({
        "success": False,
        "message": "Authentication required",
        "error": "Unauthorized access"
    }), 401