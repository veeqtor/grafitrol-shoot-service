"""Module to test for the reservation view"""

import json
import random
from datetime import datetime, timedelta
from os import getenv
from faker import Factory as FakerFactory

from src.helpers.messages import ERROR_MSG, SUCCESS_MSG
from src.helpers.shoots_slots import get_localized_slots
from src.models import Reservation
from src.models.reservations import ReservationStatusChoices
from tests.factories import (ShootFactory, CoordinatorFactory,
                             ReservationsFactory)

faker = FakerFactory.create()

BASE_URL = getenv('BASE_URL_V1')
reservation_url = BASE_URL + '/reservation'


class TestReservationView:
    """Test the reservation view"""
    def create_reservation_payload(self):
        """reservation payload"""
        shoot = ShootFactory()
        coordinator = CoordinatorFactory()
        date_string = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        slots = get_localized_slots(coordinator.get_slots_by_date(date_string))
        return {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "additionalInfo": faker.sentence(nb_words=5),
            "reservationDatetime": slots[random.randrange(0, 4, 1)],
            "duration": shoot.duration,
            "coordinatorId": coordinator.id,
            "shootId": shoot.id,
        }

    def test__create_reservation_succeeds(self, client, db_session):
        """Should create a reservation."""

        payload = self.create_reservation_payload()
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 201
        assert response_json['message'] == SUCCESS_MSG['SYS_001']
        assert response_json.get('data')
        assert Reservation.exists(response_json['data']['id'])
        assert response_json['data']['status'] == \
               ReservationStatusChoices.pending.name

    def test__create_reservation_with_already_reserved_date_fails(
            self, client, db_session):
        """Should fail to create a reservation with an already reserved day."""

        reservation = ReservationsFactory()
        payload = self.create_reservation_payload()
        payload['coordinatorId'] = reservation.coordinator.id
        payload['reservationDatetime'] = str(reservation.reservation_datetime)

        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        error = response_json.get('error')
        assert response_json['message'] == ERROR_MSG['SYS_001']
        assert error == ERROR_MSG['RES_001']

    def test__create_reservation_with_invalid_payload_fails(
            self, client, db_session):
        """Should fail to create a reservation with invalid payload."""

        payload = {}
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 400
        error = response_json.get('error')
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert error
        assert error['coordinatorId'][0] == ERROR_MSG['SYS_010']
        assert error['duration'][0] == ERROR_MSG['SYS_010']
        assert error['email'][0] == ERROR_MSG['SYS_010']
        assert error['firstName'][0] == ERROR_MSG['SYS_010']
        assert error['lastName'][0] == ERROR_MSG['SYS_010']
        assert error['phone'][0] == ERROR_MSG['SYS_010']
        assert error['reservationDatetime'][0] == ERROR_MSG['SYS_010']
        assert error['shootId'][0] == ERROR_MSG['SYS_010']

    def test__create_reservation_with_wrong_duration_fails(
            self, client, db_session):
        """Should fail to create a reservation with invalid duration."""

        payload = self.create_reservation_payload()
        payload['duration'] = 200
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_001']
        assert response_json.get('error') == ERROR_MSG['RES_003']

    def test__create_reservation_invalid_shoot_id_fails(
            self, client, db_session):
        """Should fail to create a reservation with invalid shoot id"""

        payload = self.create_reservation_payload()
        payload['shootId'] = '-MIWGuQNCS80aVH56eq'
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        error = response_json.get('error')
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert error
        assert error['shootId'][0] == ERROR_MSG['SYS_004'].format(20)
        assert error['shootId'][1] == ERROR_MSG['SYS_006']

    def test__create_reservation_invalid_coordinator_id_fails(
            self, client, db_session):
        """Should fail to create a reservation with invalid coordinator id"""

        payload = self.create_reservation_payload()
        payload['coordinatorId'] = '-MIWGuQNCS80aVH56eq'
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        error = response_json.get('error')
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']
        assert error
        assert error['coordinatorId'][0] == ERROR_MSG['SYS_004'].format(20)
        assert error['coordinatorId'][1] == ERROR_MSG['SYS_006']

    def test__create_reservation_unknown_coordinator_id_fails(
            self, client, db_session):
        """Should fail to create a reservation with unknown coordinator id"""

        payload = self.create_reservation_payload()
        payload['coordinatorId'] = '-MIWGuQNCS80aVH56eqX'
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        error = response_json.get('error')
        assert response_raw.status_code == 404
        assert response_json['message'] == ERROR_MSG['SYS_001']
        assert error == ERROR_MSG['SYS_009'].format('Coordinator')

    def test__create_reservation_unknown_shootId_id_fails(
            self, client, db_session):
        """Should fail to create a reservation with unknown shoot id"""

        payload = self.create_reservation_payload()
        payload['shootId'] = '-MIWGuQNCS80aVH56eqX'
        response_raw = client.post(reservation_url,
                                   data=json.dumps(payload),
                                   content_type="application/json")
        response_json = json.loads(response_raw.data)
        error = response_json.get('error')
        assert response_raw.status_code == 404
        assert response_json['message'] == ERROR_MSG['SYS_001']
        assert error == ERROR_MSG['SYS_009'].format('Shoot')

    def test__update_reservation_status_succeeds(self, client, db_session):
        """Should update the reservation status."""

        reservation = ReservationsFactory(
            status=ReservationStatusChoices.pending)

        assert reservation.status == ReservationStatusChoices.pending

        payload = {"status": "cancelled"}
        url = reservation_url + '/' + reservation.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)

        assert response_raw.status_code == 200
        assert response_json['message'] == SUCCESS_MSG['SYS_003']
        assert response_json.get('data')

        assert reservation.status == ReservationStatusChoices.cancelled
        assert response_json['data']['status'] == \
               ReservationStatusChoices.cancelled.name

    def test__update_reservation_status_fails(self, client, db_session):
        """Should fail when a user tries to update reservation status to
		other status type except `cancelled`."""

        reservation = ReservationsFactory(
            status=ReservationStatusChoices.pending)

        assert reservation.status == ReservationStatusChoices.pending

        payload = {"status": "completed"}

        url = reservation_url + '/' + reservation.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 401
        assert response_json['message'] == ERROR_MSG['SYS_001']
        assert response_json.get('error') == ERROR_MSG['RES_002']

    def test__update_reservation_status_with_invalid_status_fails(
            self, client, db_session):
        """Should fail when a user tries to update reservation status with
		invalid status."""

        reservation = ReservationsFactory(
            status=ReservationStatusChoices.pending)

        assert reservation.status == ReservationStatusChoices.pending

        payload = {"status": "invalid"}
        url = reservation_url + '/' + reservation.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 400
        assert response_json['message'] == ERROR_MSG['SYS_002']

    def test__update_reservation_status_with_cancelled_status_fails(
            self, client, db_session):
        """Should fail when a user tries to update reservation status that
		is already cancelled."""

        reservation = ReservationsFactory(
            status=ReservationStatusChoices.cancelled)

        assert reservation.status == ReservationStatusChoices.cancelled

        payload = {"status": "completed"}
        url = reservation_url + '/' + reservation.id
        response_raw = client.patch(url,
                                    data=json.dumps(payload),
                                    content_type="application/json")
        response_json = json.loads(response_raw.data)
        assert response_raw.status_code == 401
        assert response_json['error'] == ERROR_MSG['RES_002']
        assert response_json['message'] == ERROR_MSG['SYS_001']
