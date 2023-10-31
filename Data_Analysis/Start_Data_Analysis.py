import os
import sys
####獲取當前文件目錄####
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
#######################
import json
from datetime import datetime
from datetime import timedelta
import wifi_client_filter_out_device as WCFOD
import Stay_Point_Movement_Path_Categorization as SPMPC

for i in range(30):
    start_time=1696089600+86400*i
    endtime=1696175999+86400*i
    SPMPC.Stay_Point_Movement_path("Client","path",start_time,endtime)
