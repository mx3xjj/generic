import pytz
from datetime import datetime

def convert_datetimestr_to_timestamp(time_str):
    # check if is valid datetime passed
    if time_str.count(" ") != 2:
        raise CreatePromotionError('invalid datetime string <{}> from config, should be in format <02/14/2020 00:00:00 America/Los_Angeles>')
    datetime_str, timezone_str = time_str.rsplit(' ', maxsplit=1)
    timezone_obj = pytz.timezone(timezone_str)
    return datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S').replace(tzinfo=timezone_obj)

# call func
convert_datetimestr_to_timestamp("02/14/2020 00:00:00 America/Los_Angeles")

# all valid timezone str
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
print(pytz.all_timezones)
