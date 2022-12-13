# import calendar, datetime
# def time_in_range(start, end, x):
#     """Return true if x is in the range [start, end]"""
#     if start <= end:
#         return start <= x <= end
#     else:
#         return start <= x or x <= end
# today = datetime.datetime.today()
# print(time_in_range(datetime.time(2,11,3),datetime.time(3,0,3),today.time()))
import random
import string
# for i in range(0, 50):
#     ret = str(random.randint(50, 59)) + ''.join(random.choices(string.ascii_uppercase, k=1))+'-'+''.join(random.choices(string.digits, k=5))
#     print(ret)

for i in range(0, 50):
    print(''.join(random.choices(string.digits+string.ascii_uppercase, k=6)))
