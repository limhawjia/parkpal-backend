# Python program to pull, normalize and store HDB parking data.

from datetime import datetime
import pytz

singapore_timezone = pytz.timezone('Asia/Singapore')
current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
print("Hello world! It is now " + current_datetime)
