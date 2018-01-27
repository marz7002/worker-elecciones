# coding: utf-8

import datetime

from pytz import timezone
from dateutil.tz import tzutc


# getting today date in mexico
def get_today_mex():
    today = datetime.datetime.utcnow()
    today = today.replace(tzinfo=tzutc())
    today = today.astimezone(timezone('America/Mexico_City'))

    return today


# converting date to Mexico
def convert_to_mex(date):
    date = date.replace(tzinfo=tzutc())
    date = date.astimezone(timezone('America/Mexico_City'))

    return date