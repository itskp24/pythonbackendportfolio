"""
API routes for contact form operations
"""
import logging
from flask import Blueprint, request, jsonify
from services.auth import auth
from services.contact_service import ContactService
from utils.validators import validate_contact_input
from utils.response_helpers import make_response
from config import API_PREFIX

# Create blueprint for contact routes
contact_bp = Blueprint('contacts', __name__, url_prefix=f'{API_PREFIX}/contacts')
logger = logging.getLogger(__name__)

@contact_bp.route('', methods=['POST'])
def create_contact():
    """
    API endpoint to create a new contact form submission
    
    Request body:
        - name (str): Name of the sender (required)
        - email (str): Email of the sender (required)
        - message (str): Message content (required)
        - phone (str): Phone number of the sender (optional)
        
    Returns:
        JSON response with the created contact data
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return make_response(success=False, message="No JSON data provided", status_code=400)
        
        # Validate input data
        validation_result = validate_contact_input(data)
        if not validation_result['valid']:
            return make_response(
                success=False, 
                message=validation_result['message'], 
                status_code=400
            )
        
        # Create contact using service
        contact_data, status_code = ContactService.create_contact(data)
        
        if status_code != 201:
            return make_response(success=False, message=contact_data.get('error', 'Failed to create contact submission'), status_code=status_code)
        
        return make_response(
            success=True,
            message="Contact submission received successfully",
            data=contact_data,
            status_code=201
        )
    
    except Exception as e:
        logger.error(f"Error in create_contact endpoint: {str(e)}")
        return make_response(success=False, message=f"Server error: {str(e)}", status_code=500)

@contact_bp.route('', methods=['GET'])
@auth.login_required
def get_contacts():
    """
    API endpoint to get a list of contact submissions
    
    This endpoint requires authentication
    
    Query parameters:
        - limit (int): Maximum number of contacts to return (default: 100)
        - offset (int): Offset for pagination (default: 0)
        
    Returns:
        JSON response with the list of contact submissions
    """
    try:
        # Get query parameters for pagination
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get contacts using service
        result, status_code = ContactService.get_all_contacts(limit, offset)
        
        if status_code != 200:
            return make_response(success=False, message=result.get('error', 'Failed to retrieve contact submissions'), status_code=status_code)
        
        return make_response(
            success=True,
            message="Contact submissions retrieved successfully",
            data=result,
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error in get_contacts endpoint: {str(e)}")
        return make_response(success=False, message=f"Server error: {str(e)}", status_code=500)

@contact_bp.route('/<int:contact_id>', methods=['GET'])
@auth.login_required
def get_contact(contact_id):
    """
    API endpoint to get a single contact submission by ID
    
    This endpoint requires authentication
    
    Path parameters:
        - contact_id (int): ID of the contact submission to retrieve
        
    Returns:
        JSON response with the contact submission data
    """
    try:
        # Get contact using service
        contact_data, status_code = ContactService.get_contact_by_id(contact_id)
        
        if status_code != 200:
            return make_response(success=False, message=contact_data.get('error', 'Failed to retrieve contact submission'), status_code=status_code)
        
        return make_response(
            success=True,
            message="Contact submission retrieved successfully",
            data=contact_data,
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error in get_contact endpoint: {str(e)}")
        return make_response(success=False, message=f"Server error: {str(e)}", status_code=500)