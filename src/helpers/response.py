"""Response handler"""

from typing import Dict, Tuple

from src.helpers.messages import ERROR_MSG, SUCCESS_MSG


class ResponseHandler(object):
    """
	Class that handles all API responses.
	"""
    def __init__(self,
                 data=None,
                 msg_key=None,
                 status_code=200,
                 status='success'):
        self.data = data
        self.msg_key = msg_key
        self.status = status
        self.status_code = status_code

        self.output = {
            'status': 'success',
            'data': self.data,
        }

    def get_response(self) -> Tuple[Dict[str, str], int]:
        """
		Response helper for response messages.
		"""

        if self.msg_key is None and self.status == 'error':
            self.output['status'] = 'error'
            if self.data:
                del self.output['data']
                self.output['error'] = self.data
            return self.output, self.status_code

        elif self.msg_key is not None and self.status == 'error':
            self.output['status'] = 'error'
            self.output['message'] = ERROR_MSG[self.msg_key]
            if self.data:
                del self.output['data']
                self.output['error'] = self.data
            return self.output, self.status_code

        if self.msg_key is None:
            return self.output, self.status_code

        self.output['message'] = SUCCESS_MSG[self.msg_key]
        return self.output, self.status_code
