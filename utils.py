import datetime as dt
import time
import pytz


def unix_ts_to_datetime(ts=0, timezone='Europe/Kyiv'):
    return dt.datetime.fromtimestamp(ts, pytz.timezone(timezone))


def get_current_time(timezone='Europe/Kyiv'):
    return unix_ts_to_datetime(int(time.time()), timezone)

