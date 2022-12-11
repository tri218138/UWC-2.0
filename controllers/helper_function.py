import calendar, datetime
import random
import string

MORNING_SHIFT = (datetime.time(8,0,0), datetime.time(11,0,0))
AFTERNOON_SHIFT = (datetime.time(14,0,0), datetime.time(18,0,0))
COLOR_GROUP = [
    "#ff0000", # mcp0
    "#2200ff", # group1
    "#f6ff00", # group2
    "#00e5d6", # group3
    "#00ff87", # group4
    "#ffbb00", # group5
]

def getCurrentDateTime():
    return datetime.datetime(2022, 12, 11, 11, 52, 10)
    return datetime.datetime.today()

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def generate_employee_id():
    return ''.join(random.choices(string.digits+string.ascii_uppercase, k=6))