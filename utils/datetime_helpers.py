"""All datetime helpers"""

import logging
from dateutil import parser
from datetime import datetime

from main import local_tz, utc
from utils.exceptions import ResponseException


def localize_datetime(datetime):
    """Localize dates"""
    return datetime.astimezone(tz=local_tz)


def convert_to_utc(localized_datetime):
    """Convert datetime to utc"""
    return localized_datetime.astimezone(tz=utc)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def date_validator(date_value):
    """Validates date format

     Arguments:
        date_value (string): date string

     Raises:
        ValidationError: Used to raise exception if date format is not valid

    Returns:
        date: the validated date
    """
    try:
        parser.parse(date_value).date()
        date = datetime.strptime(date_value, '%Y-%m-%d')
        return date
    except ValueError as e:
        logger.error(e)
        raise ResponseException(e, 400)
