"""
Service to handle contact form submissions
"""
import logging
import time
import os
from datetime import datetime
try:
    from sqlalchemy.exc import SQLAlchemyError, OperationalError
except ImportError:
    # Fallback for when direct import isn't working
    from sqlalchemy import exc
    SQLAlchemyError = exc.SQLAlchemyError
    OperationalError = exc.OperationalError
from app import db
from models import Contact

logger = logging.getLogger(__name__)

# Maximum retry attempts for database operations
MAX_RETRIES = int(os.environ.get("DB_MAX_RETRIES", "3"))
RETRY_DELAY = float(os.environ.get("DB_RETRY_DELAY", "0.5"))  # seconds

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
        
        # Implement retry logic for database operations
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Add to database and commit
                db.session.add(new_contact)
                db.session.commit()
                
                # Return the created contact as dictionary
                return new_contact.to_dict(), 201
                
            except OperationalError as e:
                # This is likely a connection issue, retry
                retries += 1
                error_message = str(e)
                logger.warning(f"Database connection error (attempt {retries}/{MAX_RETRIES}): {error_message}")
                
                # Rollback the session
                db.session.rollback()
                
                if retries < MAX_RETRIES:
                    # Wait before retrying
                    time.sleep(RETRY_DELAY * retries)  # Exponential backoff
                else:
                    # Log the final failure
                    logger.error(f"Failed to create contact after {MAX_RETRIES} attempts: {error_message}")
                    
                    # User-friendly error message for connection issues
                    return {"error": "Database connection error. Please try again later."}, 503
                    
            except SQLAlchemyError as e:
                # Other database errors - no retry
                db.session.rollback()
                error_message = str(e)
                logger.error(f"Database error creating contact: {error_message}")
                return {"error": "Database error occurred. Please try again later."}, 500
                
            except Exception as e:
                # General errors - no retry
                db.session.rollback()
                error_message = str(e)
                logger.error(f"Error creating contact: {error_message}")
                return {"error": "Failed to create contact. Please try again."}, 500
    
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
        # Implement retry logic for database operations
        retries = 0
        while retries < MAX_RETRIES:
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
                
            except OperationalError as e:
                # This is likely a connection issue, retry
                retries += 1
                error_message = str(e)
                logger.warning(f"Database connection error (attempt {retries}/{MAX_RETRIES}): {error_message}")
                
                # Rollback the session to be safe
                db.session.rollback()
                
                if retries < MAX_RETRIES:
                    # Wait before retrying with exponential backoff
                    time.sleep(RETRY_DELAY * retries)
                else:
                    # Log the final failure
                    logger.error(f"Failed to retrieve contacts after {MAX_RETRIES} attempts: {error_message}")
                    
                    # User-friendly error message for connection issues
                    return {"error": "Database connection error. Please try again later."}, 503
                    
            except SQLAlchemyError as e:
                # Other database errors - no retry
                db.session.rollback()
                error_message = str(e)
                logger.error(f"Database error retrieving contacts: {error_message}")
                return {"error": "Database error occurred. Please try again later."}, 500
                
            except Exception as e:
                # General errors - no retry
                error_message = str(e)
                logger.error(f"Error retrieving contacts: {error_message}")
                return {"error": "Failed to retrieve contacts. Please try again."}, 500
    
    @staticmethod
    def get_contact_by_id(contact_id):
        """
        Get a single contact submission by ID
        
        Args:
            contact_id (int): ID of the contact to retrieve
            
        Returns:
            tuple: (contact_dict, status_code)
        """
        # Implement retry logic for database operations
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Query contact by ID
                contact = Contact.query.get(contact_id)
                
                # Check if contact exists
                if not contact:
                    return {"error": f"Contact with ID {contact_id} not found"}, 404
                
                # Return contact as dictionary
                return contact.to_dict(), 200
                
            except OperationalError as e:
                # This is likely a connection issue, retry
                retries += 1
                error_message = str(e)
                logger.warning(f"Database connection error (attempt {retries}/{MAX_RETRIES}): {error_message}")
                
                # Rollback the session to be safe
                db.session.rollback()
                
                if retries < MAX_RETRIES:
                    # Wait before retrying with exponential backoff
                    time.sleep(RETRY_DELAY * retries)
                else:
                    # Log the final failure
                    logger.error(f"Failed to retrieve contact by ID after {MAX_RETRIES} attempts: {error_message}")
                    
                    # User-friendly error message for connection issues
                    return {"error": "Database connection error. Please try again later."}, 503
                    
            except SQLAlchemyError as e:
                # Other database errors - no retry
                db.session.rollback()
                error_message = str(e)
                logger.error(f"Database error retrieving contact by ID: {error_message}")
                return {"error": "Database error occurred. Please try again later."}, 500
                
            except Exception as e:
                # General errors - no retry
                error_message = str(e)
                logger.error(f"Error retrieving contact by ID: {error_message}")
                return {"error": "Failed to retrieve contact. Please try again."}, 500