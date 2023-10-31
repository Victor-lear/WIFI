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
##############################
import wifi_client_filter_out_device as WCFOD
import Mongo.mongo as mongo

def Stay_Point_Movement_path(DB,Collection,start_time,end_time):
   def split_data(data):
      split_data = data.split("_")
      if (len(split_data)==4):
         split_data[0]=split_data[0]+"_"+split_data[1]
         split_data[1]=split_data[2]
         split_data[2]=split_data[3]
         split_data.pop()
      return split_data
   stimestamp=1680278400
   start_time = datetime.fromtimestamp(stimestamp)
   etimestamp=1680364799
   end_time = datetime.fromtimestamp(etimestamp)
   data=WCFOD.Filter_out_device("Client","Controller4",start_time,end_time)
   user_mac=[]
   for i in range(len(data)-2):
      user_mac.append(data[i]['sta_mac_address'])

   set_user_mac=list(set(user_mac))#去除相同資料
   stay=[]
   staycont=0
   for i in range(len(set_user_mac)):
      
      # if(int(data[int(len(data)-1)][i]['ap_identifiers_count'])>=2):
            index = [u for u, value in enumerate(user_mac) if value == set_user_mac[i]]
         
            for j in range(len(index)):
               #if(type(data[index[j]]['total_data_bytes'])!=str):
                  #if(int(data[index[j]]['total_data_bytes'])>0):
                     stay_way=data[index[j]]
                     if(stay!=[]):
                        st=split_data(stay_way['ap_name'])
                        st2=split_data(stay[staycont]['ap_name'])
                        if(stay_way['sta_mac_address']!=stay[staycont]['sta_mac_address']or st[0]!=st2[0]):
                           stay.append(stay_way)
                           staycont+=1
                        else:
                           stay[staycont]["End_Datetime"]=stay_way["Datetime"]
                     else:
                        stay.append(stay_way)
   move=[]
   move_start_end=[]

   for i in range(1,len(stay)):
      if(stay[i-1]['sta_mac_address']==stay[i]['sta_mac_address']):
         try:
            Starttime=stay[i-1]['End_Datetime']
         except:
            Starttime=stay[i-1]['Datetime']
         Endtime=stay[i]['Datetime']
         if((Endtime-Starttime)<timedelta(minutes=20)):
            start_way=split_data(stay[i-1]['ap_name'])
            end_way=split_data(stay[i]['ap_name'])
            data={
                  #'sta_mac_address':stay[i]['sta_mac_address'],
                  #'client_user_name':stay[i]['client_user_name'],
                  'start_way':start_way[0],
                  'end_way':end_way[0],
                  'start_time':Starttime,
                  'end_time':Endtime
               }
            move.append(data)
            move_start_end.append(str(start_way[0])+str(end_way[0]))
   
   move_start_end_data=list(set(move_start_end))
   path_data=[]
   for i in range(len(move_start_end_data)):
      for j in range(24):
         stime=stimestamp+3600*j
         etime=stimestamp+3599+3600*j
         pathdata={
            'path':move_start_end_data[i],
            'num':0,
            'start_time':datetime.fromtimestamp(stime),
            'end_time':datetime.fromtimestamp(etime)
         }
         path_data.append(pathdata)


   for i in range(len(move)):
      v=str(move[i]['start_way'])+str(move[i]['end_way'])
      index = [u for u, value in enumerate(move_start_end_data) if value == v]
      hour=int(move[i]['start_time'].hour)
      path_data[int((24*index[0])+hour)]['num']+=1
   
   mongo.WIFI_WriteInDB(DB,Collection,path_data)
         
               
