import calendar, datetime

MORNING_SHIFT = (datetime.time(8,0,0), datetime.time(11,0,0))
AFTERNOON_SHIFT = (datetime.time(14,0,0), datetime.time(18,0,0))

def getCurrentTime():
    return datetime.datetime(2022, 12, 11, 9, 8, 10)
    return datetime.datetime.today()

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end