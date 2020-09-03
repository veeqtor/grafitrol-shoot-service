"""Custom Exceptions"""


class DataConflictException(Exception):
    """This exception is raised when a unique constraint is not met"""
    
    def __init__(self, message):
        self.message = message
