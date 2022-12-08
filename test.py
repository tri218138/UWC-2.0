import calendar, datetime

today = datetime.datetime.today()
print(calendar.monthcalendar(today.year, today.month))