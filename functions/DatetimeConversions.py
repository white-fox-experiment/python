from datetime import datetime, timedelta
from pytz import timezone
from pytz import reference
import pytz

# get current time
today = datetime.now()
#today = datetime(2019,11,15,10,0,0)

# set two timezones we want to work with
utc = pytz.timezone('UTC')
central = pytz.timezone('US/Central')

# figure out what timezone script is currently running in
local_time = reference.LocalTimezone()
current_timezone = local_time.tzname(today)
print('Current time in {} is {}'.format(current_timezone,today))

# if current timezone is not UTC convert to UTC
if current_timezone != 'Coordinated Universal Time':
    # convert time to UTC
    print("I'm not UTC; convert me to UTC")
    utc_current_time =  today.astimezone(utc)
    print('Current time in UTC is {}'.format(utc_current_time))
else:
    utc_current_time = today
    
# convert datetime to US/Central (compensates for CDT vs CST)
central_current_time = utc_current_time.astimezone(central)
print('Current time in US/Central is {}'.format(central_current_time))
