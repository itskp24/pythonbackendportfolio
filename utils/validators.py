"""
Validation utilities for API input data
"""
import re
import logging

logger = logging.getLogger(__name__)

def validate_contact_input(data):
    """
    Validate input data for contact form submissions
    
    Args:
        data (dict): Input data to validate
        
    Returns:
        dict: Validation result with 'valid' and 'message' keys
    """
    if not data:
        return {"valid": False, "message": "No data provided"}
    
    # Check required fields
    if not data.get('name'):
        return {"valid": False, "message": "Name is required"}
        
    if not data.get('email'):
        return {"valid": False, "message": "Email is required"}
        
    if not data.get('message'):
        return {"valid": False, "message": "Message is required"}
    
    # Validate name length
    if len(data.get('name', '')) > 100:
        return {"valid": False, "message": "Name must be 100 characters or less"}
    
    # Validate email format
    email = data.get('email', '')
    # Simple regex for basic email validation
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        logger.warning(f"Invalid email format: {email}")
        return {"valid": False, "message": "Invalid email format"}
    
    # Validate phone number format (if provided)
    phone = data.get('phone')
    if phone:
        if len(phone) > 20:
            return {"valid": False, "message": "Phone number must be 20 characters or less"}
        
        # Basic phone number format validation (allows various formats)
        if not re.match(r'^[\d\+\-\(\)\s\.]+$', phone):
            return {"valid": False, "message": "Invalid phone number format"}
    
    # Validate message length
    if len(data.get('message', '')) > 1000:
        return {"valid": False, "message": "Message must be 1000 characters or less"}
    
    return {"valid": True, "message": "Validation successful"}