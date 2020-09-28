"""Module to test for the flask application"""

import json


class TestFlaskApp:
    """Test the flask application"""
    def test_flask_application(self, client):
        """Should pass if the application starts successfully.
        Args:
            client (func): Flask test client
        Returns:
            None
        """

        response_raw = client.get('/')
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 200
        assert response_json['data'] is not None
