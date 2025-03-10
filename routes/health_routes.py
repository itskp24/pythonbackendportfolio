"""
Health check routes for the API
"""
import logging
from flask import Blueprint
from utils.response_helpers import make_response
from config import API_PREFIX

# Create blueprint for health routes
health_bp = Blueprint('health', __name__, url_prefix=f'{API_PREFIX}')
logger = logging.getLogger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    API endpoint to check if the API is running
    
    Returns:
        JSON response with health status
    """
    try:
        return make_response(
            success=True,
            message="API is running",
            data={
                "status": "healthy",
                "version": "1.0.0"
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error in health check endpoint: {str(e)}")
        return make_response(
            success=False,
            message="API is experiencing issues",
            data={
                "status": "unhealthy",
                "error": str(e)
            },
            status_code=500
        )