"""
Database models for the application
"""
import logging
from datetime import datetime
from app import db

logger = logging.getLogger(__name__)

class Contact(db.Model):
    """
    Model for storing contact form submissions
    """
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, name, email, message, phone=None):
        self.name = name
        self.email = email
        self.message = message
        self.phone = phone
    
    def to_dict(self):
        """
        Convert model to dictionary for API responses
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Contact {self.id}: {self.name}>'