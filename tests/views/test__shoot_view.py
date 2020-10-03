"""Module to test for the shoot view"""

import json
from os import getenv

from src.helpers.messages import ERROR_MSG, SUCCESS_MSG
from src.models import Shoot

BASE_URL = getenv('BASE_URL_V1')
shoot_url = BASE_URL + '/shoot'


class TestShootView:
    """Test the shoot view"""
    def test__create_shoot_succeeds(self, client, db_session):
        """Should create a shoot."""
        payload = {
            "name": "Shoot type",
            "description": "Shoot description",
            "duration": 60,
            "price": 5000
        }
        response_raw = client.post(shoot_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 201
        assert response_json['message'] == SUCCESS_MSG['SYS_001']
        assert response_json.get('data')
        assert Shoot.exists(response_json['data']['id'])

    def test__create_shoot_with_missing_fields_fails(self, client, db_session):
        """Should create a shoot."""

        payload = {
            "name": "Shoot type",
            "description": "Shoot description",
            "duration": 60
        }
        response_raw = client.post(shoot_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert response_json['error']['price'][0] == ERROR_MSG['SYS_008']

    def test__update_shoot_succeeds(self, client, new_shoots):
        """Should update a shoot."""
        shoot = new_shoots[0]
        payload = {
            "name": "Shoot type II",
            "description": "Shoot description II",
            "duration": 120
        }

        url = shoot_url + '/' + shoot.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['message'] == SUCCESS_MSG['SYS_003']
        assert response_json.get('data')
        assert response_json['data']['name'] == payload['name'].capitalize()
        assert response_json['data']['duration'] == payload['duration']

    def test__delete_shoot_succeeds(self, client, new_shoots):
        """Should delete a shoot."""

        shoot = new_shoots[1]
        url = shoot_url + '/' + shoot.id
        response_raw = client.delete(url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['message'] == SUCCESS_MSG['SYS_002']
        assert response_json.get('data')
        assert not Shoot.exists(response_json['data']['id'])

    def test__list_shoots_succeeds(self, client, new_shoots):
        """Should get a list of shoots."""

        response_raw = client.get(shoot_url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert len(response_json['data']) == 10

    def test__get_a_shoot_succeeds(self, client, new_shoots):
        """Should get a single of shoot."""

        shoot = new_shoots[0]
        url = shoot_url + '/' + shoot.id
        response_raw = client.get(url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['data']
        assert response_json['data']['id'] == shoot.id
        assert response_json['data']['name'] == shoot.name

    def test__get_a_shoot_with_invalid_id_fails(self, client, db_session):
        """Should throw an error when an invalid ID is provided."""

        url = shoot_url + '/' + 'invalid'
        response_raw = client.get(url)
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert response_json['error'][0] == ERROR_MSG['SYS_006']
