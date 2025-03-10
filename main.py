"""
Entry point for the Flask application
"""
import logging
from app import app
from config import API_PORT

logger = logging.getLogger(__name__)

# Run the application
if __name__ == "__main__":
    logger.info(f"Starting Flask API server on port {API_PORT}")
    app.run(host="0.0.0.0", port=API_PORT, debug=True)