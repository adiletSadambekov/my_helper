from datetime import datetime, time, timedelta
import pytz


def get_interval(point_time: time, time_zone: str) -> timedelta:
    tz_info = pytz.timezone(time_zone)
    now = datetime.now(tz_info)
    point_of_sends = datetime(
        now.year,
        now.month,
        now.day,
        point_time.hour,
        point_time.minute)
    interval = tz_info.localize(point_of_sends) - now
    return interval