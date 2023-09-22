import os
import sys
####獲取當前文件目錄####
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
#######################
import json
from datetime import datetime
##############################
import wifi_client_filter_out_device as WCFOD
import Mongo.mongo as mongo

timestamp=1680278400
start_time = datetime.fromtimestamp(timestamp)
timestamp=1680969599
end_time = datetime.fromtimestamp(timestamp)
data=WCFOD.Filter_out_device("AP","April",start_time,end_time)
user_name=[]
for i in range(len(data)-2):
   user_name.append(data[i]['client_user_name'])

for i in range(len(data[len(data)-1])):
    if(int(data[len(data)-1][i]['ap_identifiers_count'])>=2):
         index = [i for i, value in enumerate(user_name) if value == data[len(data)-1][i]['user_name']]
         for i in range(len(index)):
            if(data[index[i]]['total_data_bytes']>0):
               print(data[index[i]])
              
        
# timestamp=1680278400
# start_time = datetime.fromtimestamp(timestamp)
# timestamp=1680969599
# end_time = datetime.fromtimestamp(timestamp)
# data={
#     'client_user_name':'9a:35:22:f9:5d:12',
#     "Datetime": {"$gte": start_time, "$lte": end_time}
# }

# data=mongo.WIFI_FindData('AP_test','April_Client',data)
# mongo.WIFI_WriteInDB('AP_test','test_data',data)
