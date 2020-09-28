"""Module to test for the coordinator view"""

import json
from os import getenv
from datetime import datetime, timedelta

from src.helpers.messages import ERROR_MSG, SUCCESS_MSG
from src.models import Coordinator

BASE_URL = getenv('BASE_URL_V1')
coordinator_url = BASE_URL + '/coordinator'
coordinator_url_date = coordinator_url + '?date={}'


class TestCoordinatorView:
    """Test the flask application"""
    def test__create_coordinator_succeeds(self, client, db_session):
        """Should create a coordinator."""
        payload = {
            "breakDuration": 60,
            "breakStartTime": "12:00",
            "endOfDay": "18:00",
            "startOfDay": "7:00",
            "user": "Sample New TestUser"
        }
        response_raw = client.post(coordinator_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 201
        assert response_json['message'] == SUCCESS_MSG['SYS_001']
        assert response_json.get('data')
        assert Coordinator.exists(response_json['data']['id'])

    def test__create_coordinator_with_missing_fields_fails(
            self, client, db_session):
        """Should create a coordinator."""
        payload = {
            "breakStartTime": "12:00",
            "endOfDay": "18:00",
            "startOfDay": "7:00",
            "user": "Sample New TestUser"
        }
        response_raw = client.post(coordinator_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert response_json['error']['breakDuration'][0] == ERROR_MSG[
            'SYS_008']

    def test__update_coordinator_succeeds(self, client, new_coordinators):
        """Should update a coordinator."""
        coordinator = new_coordinators[0]
        payload = {
            "breakDuration": 240,
            "startOfDay": "10:00:00",
        }

        url = coordinator_url + '/' + coordinator.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['message'] == SUCCESS_MSG['SYS_003']
        assert response_json.get('data')
        assert response_json['data']['startOfDay'] == payload['startOfDay']
        assert response_json['data']['breakDuration'] == payload[
            'breakDuration']

    def test__delete_coordinator_succeeds(self, client, new_coordinators):
        """Should delete a coordinator."""

        coordinator = new_coordinators[1]
        url = coordinator_url + '/' + coordinator.id
        response_raw = client.delete(url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['message'] == SUCCESS_MSG['SYS_002']
        assert response_json.get('data')
        assert not Coordinator.exists(response_json['data']['id'])

    def test__list_coordinators_succeeds(self, client, new_coordinators):
        """Should get a list of coordinators."""

        response_raw = client.get(coordinator_url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert len(response_json['data']) == 10

    def test__get_a_coordinator_succeeds(self, client, new_coordinators):
        """Should get a single of coordinators."""

        coordinator = new_coordinators[0]
        url = coordinator_url + '/' + coordinator.id
        response_raw = client.get(url)
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['data']
        assert response_json['data']['id'] == coordinator.id
        assert response_json['data']['startOfDay'] == \
               str(coordinator.start_of_day)
        assert response_json['data']['endOfDay'] == str(coordinator.end_of_day)

    def test__get_a_coordinator_with_invalid_id_fails(self, client,
                                                      db_session):
        """Should throw an error when an invalid ID is provided."""

        url = coordinator_url + '/' + 'invalid'
        response_raw = client.get(url)
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert response_json['error'][0] == ERROR_MSG['SYS_006']

    def test__coordinator_succeeds(self, client, new_coordinators):
        """Should pass if a coordinator is available for the selected date"""

        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response_raw = client.get(coordinator_url_date.format(date))
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json is not None

    def test__coordinator_return_400_fails(self, client, db_session):
        """Should fail if no coordinator is available."""

        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response_raw = client.get(coordinator_url_date.format(date))
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['CO_001']

    def test__coordinator_invalid_date_param_fails(self, client, db_session):
        """Should fail if no date param was provided."""

        response_raw = client.get(coordinator_url_date.format('2020-10-90'))
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 400
        assert response_json['error'] == ERROR_MSG['SYS_003']
