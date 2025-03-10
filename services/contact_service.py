"""
Service to handle contact form submissions
"""
import logging
from datetime import datetime
from app import db
from models import Contact

logger = logging.getLogger(__name__)

class ContactService:
    """
    Service class for contact form submission operations
    """
    
    @staticmethod
    def create_contact(contact_data):
        """
        Create a new contact submission in the database
        
        Args:
            contact_data (dict): Data for creating the contact submission
            
        Returns:
            tuple: (contact_dict, status_code)
        """
        try:
            # Extract data from the request
            name = contact_data.get('name')
            email = contact_data.get('email')
            message = contact_data.get('message')
            phone = contact_data.get('phone')
            
            # Create a new contact instance
            new_contact = Contact(
                name=name,
                email=email,
                message=message,
                phone=phone
            )
            
            # Add to database and commit
            db.session.add(new_contact)
            db.session.commit()
            
            # Return the created contact as dictionary
            return new_contact.to_dict(), 201
            
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            logger.error(f"Error creating contact: {str(e)}")
            return {"error": f"Failed to create contact: {str(e)}"}, 500
    
    @staticmethod
    def get_all_contacts(limit=100, offset=0):
        """
        Get a list of all contact submissions from the database
        
        Args:
            limit (int): Maximum number of contacts to return
            offset (int): Offset for pagination
            
        Returns:
            tuple: (contacts_list, status_code)
        """
        try:
            # Query contacts with pagination
            contacts = Contact.query.order_by(Contact.created_at.desc()).limit(limit).offset(offset).all()
            
            # Convert list of contacts to list of dictionaries
            contacts_list = [contact.to_dict() for contact in contacts]
            
            # Get total count for pagination info
            total_count = Contact.query.count()
            
            # Prepare response data
            result = {
                "contacts": contacts_list,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset
                }
            }
            
            return result, 200
            
        except Exception as e:
            logger.error(f"Error retrieving contacts: {str(e)}")
            return {"error": f"Failed to retrieve contacts: {str(e)}"}, 500
    
    @staticmethod
    def get_contact_by_id(contact_id):
        """
        Get a single contact submission by ID
        
        Args:
            contact_id (int): ID of the contact to retrieve
            
        Returns:
            tuple: (contact_dict, status_code)
        """
        try:
            # Query contact by ID
            contact = Contact.query.get(contact_id)
            
            # Check if contact exists
            if not contact:
                return {"error": f"Contact with ID {contact_id} not found"}, 404
            
            # Return contact as dictionary
            return contact.to_dict(), 200
            
        except Exception as e:
            logger.error(f"Error retrieving contact by ID: {str(e)}")
            return {"error": f"Failed to retrieve contact: {str(e)}"}, 500