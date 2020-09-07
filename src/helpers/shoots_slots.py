"""Shoot booking helper"""

from datetime import datetime, timedelta, date

from main import local_tz, utc
from utils.datetime_helpers import localize_datetime

INTERVAL = 15


def get_datetime_and_capacity(start, end, interval, day=None):
    """Gets the start, end datetime and the slot
	capacity for the day

	Args:
		start (datetime.time): Start time for the day
		end (datetime.time): End time for the day
		day (date): Date
		interval (int): The session intervals in minutes

	Returns:
		capacity (int): The max capacity for the day.
		start_datetime (datetime): The start datetime in UTC
		end_datetime (datetime): The end datetime in UTC
	"""

    today = date.today()
    if day:
        today = day

    end_time = end.replace(tzinfo=local_tz)
    start_time = start.replace(tzinfo=local_tz)
    start_datetime = (datetime.combine(today, start_time)).astimezone(tz=utc)
    end_datetime = (datetime.combine(today, end_time)).astimezone(tz=utc)
    work_hour_delta = end_datetime - start_datetime
    capacity = work_hour_delta // timedelta(minutes=interval)
    return capacity, start_datetime, end_datetime


def generate_slots(start, capacity):
    """This generates all slots for the day based on the start datetime,
	capacity for the day and the intervals between sessions.

	Args:
		start (datetime): The start datetime in UTC
		capacity (int): The max capacity for the day.

	Returns:
		A generator containing all slots
	"""

    curr = start
    i = 0
    while i != capacity:
        next_datetime = curr + timedelta(minutes=INTERVAL)
        # TODO: Add more checks to determine if a slot is available for
        #  booking
        data = {'slot': curr, 'availability': False}
        if datetime.now(tz=utc) < curr:
            data['availability'] = True
        yield data
        i += 1
        curr = next_datetime


def filter_slots(reserved_shoots, break_duration, break_start_time, day,
                 slots):
    """Modifies the slots to indicate which is available or not.

	Args:
		reserved_shoots: All reserved session for the day.
		break_duration(int): Coordinator break duration
		break_start_time(time): Coordinator break time
		day (datetime): Selected date.
		slots: Generator of slots.

	Returns:
		filtered slots (Generator): Updated Generator of slots with proper
		availability
	"""
    slots_copy = [slot for slot in slots]
    for shoot in reserved_shoots:
        try:
            dt = shoot.reservation_datetime
            while dt < shoot.reservation_end_datetime:
                slot = next(filter(lambda x: x['slot'] == dt, slots_copy))
                if slot:
                    slot['availability'] = False
                dt = dt + timedelta(minutes=INTERVAL)
        except StopIteration:
            pass

    return filter_out_break_time(break_duration, break_start_time, slots_copy,
                                 day)


def filter_out_break_time(break_duration, break_start_time, slots, day=None):
    """This method filter out the break times out of the coordinators slot.

	Args:
		break_duration(int): Coordinator break duration
		break_start_time(time): Coordinator break time
		day (datetime): Selected date.
		slots: Array of slots.
		day (string): The date_value

	Returns:
		filtered slots (Generator): Updated slot array accounting for
		break time.
	"""

    validated_day = date.today()
    if day:
        validated_day = day
    start_time = break_start_time.replace(tzinfo=local_tz)
    start_datetime = (datetime.combine(validated_day,
                                       start_time)).astimezone(tz=utc)
    end_datetime = start_datetime + timedelta(minutes=break_duration)

    for slot in slots:
        dt = start_datetime
        while dt < end_datetime:
            if slot['slot'] == dt:
                slot['availability'] = False
            dt = dt + timedelta(minutes=INTERVAL)
        yield slot


def filter_and_convert_to_localtime(slots):
    """
	Filters available slots and converts the date time
	to the local timezone
	"""
    return list(
        map(lambda x: str(localize_datetime(x['slot'])),
            filter(lambda x: x['availability'], slots)))


def get_localized_slots(slots):
    """Gets the filtered localized slot datetime
	"""
    return filter_and_convert_to_localtime(slots)


def get_preferred_coordinator(coordinators, date):
    """
	Gets the most available coordinator for the date chosen
	Args:
		coordinators: List of all available coordinators
		date(string): The date string `YYYY-MM-DD`
	Returns:
		Tuple: coordinator, datetime array
	"""

    preferred_coordinator = None
    number_of_available_slots = 0

    # TODO: modify the algo to compensate for coordinators level of
    #  experience, session type and coordinators ratings. for now it just
    #  gets the coordinator with the most free slots
    for qs in coordinators:
        slots = qs.get_slots_by_date(date)
        max_slot = 0
        i = 0
        while i < len(slots):
            if slots[i]['availability']:
                max_slot += 1
            i += 1
        if max_slot > number_of_available_slots:
            number_of_available_slots = max_slot
            # This coordinator has the most free slots
            preferred_coordinator = qs

    if preferred_coordinator:
        slots = preferred_coordinator.get_slots_by_date(date)
        return preferred_coordinator, get_localized_slots(slots)
    return None
