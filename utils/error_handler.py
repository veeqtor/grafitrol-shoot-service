"""Error Handler"""

from marshmallow import ValidationError

from src.helpers.response import ResponseHandler
from utils.exceptions import DataConflictException, ResponseException


def error_handlers(app):
    """Error handlers"""
    @app.errorhandler(ValidationError)
    def handle_errors(error):
        """Handles validation errors"""

        if '_schema' in error.messages:
            error.messages = error.messages['_schema']

        response = ResponseHandler(status='error',
                                   msg_key='SYS_002',
                                   data=error.messages,
                                   status_code=400).get_response()
        return response

    @app.errorhandler(DataConflictException)
    def handle_data_conflict(e):
        """Handle data conflict exception"""
        response = ResponseHandler(status='error',
                                   msg_key='SYS_001',
                                   data=e.message,
                                   status_code=409).get_response()
        return response

    @app.errorhandler(ResponseException)
    def handle_data_conflict(e):
        """Handle data conflict exception"""
        response = ResponseHandler(status='error',
                                   msg_key='SYS_001',
                                   data=e.message,
                                   status_code=e.status_code).get_response()
        return response
