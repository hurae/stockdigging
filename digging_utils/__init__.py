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


def get_yesterday(trade_date):
    yesterday_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d') - datetime.timedelta(days=1)
    return yesterday_date.strftime('%Y%m%d')


# get date string from timestamp, specially divided by 1000 for xueqiu
def get_date_from_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp( timestamp / 1000).strftime( "%Y%m%d" )


def get_today_format():
    return datetime.date.today().strftime('%Y-%m-%d')


def get_year_format():
    last_year_date = datetime.date.today() - datetime.timedelta(days=365)
    return last_year_date.strftime('%Y-%m-%d')
