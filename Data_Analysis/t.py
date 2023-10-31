import time 
from datetime import datetime
from datetime import timedelta
timestamp=1680278400
start_time = datetime.fromtimestamp(timestamp)
timestamp=1680364799
end_time = datetime.fromtimestamp(timestamp)
print((end_time-start_time)>timedelta(minutes=20))