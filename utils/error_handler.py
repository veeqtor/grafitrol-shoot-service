"""Error Handler"""

from marshmallow import ValidationError
from utils.exceptions import DataConflictException


def error_handlers(app):
    """Error handlers"""
    
    @app.errorhandler(ValidationError)
    def handle_errors(error):
        """Handles validation errors"""
        
        if '_schema' in error.messages:
            error.messages = error.messages['_schema']
        return {
            'errors': error.messages,
            'message': 'invalid fields'
        }, 400

    @app.errorhandler(DataConflictException)
    def handle_data_conflict(e):
        """Handle data conflict exception"""
        
        return {'message': e.message}, 409
