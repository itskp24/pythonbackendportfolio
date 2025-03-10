"""
Helper functions for API responses
"""
from flask import jsonify

def make_response(success, message, data=None, status_code=200):
    """
    Create a consistent JSON response format
    
    Args:
        success (bool): Whether the operation was successful
        message (str): Message to include in the response
        data (any, optional): Data to include in the response
        status_code (int, optional): HTTP status code
        
    Returns:
        Response: Flask response with JSON data
    """
    response = {
        "success": success,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code