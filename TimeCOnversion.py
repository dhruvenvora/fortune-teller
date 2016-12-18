import datetime
import calendar
aprilFirst=datetime.datetime(2016, 06, 13, 03, 00,0)
print calendar.timegm(aprilFirst.timetuple())