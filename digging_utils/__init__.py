# this file contains some little useful tools

import datetime


# get exact time string
def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# get the date string of today
def get_today():
    return datetime.date.today().strftime('%Y%m%d')


# get the date string of the day which is 365 days ago
def get_year():
    last_year_date = datetime.date.today() - datetime.timedelta(days=365)
    return last_year_date.strftime('%Y%m%d')


# get date string from timestamp
def get_date_from_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y%m%d")
