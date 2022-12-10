import calendar, datetime
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
today = datetime.datetime.today()
print(time_in_range(datetime.time(2,11,3),datetime.time(3,0,3),today.time()))