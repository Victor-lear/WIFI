import os
import sys
####獲取當前文件目錄####
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
#######################
from bson import ObjectId
import pymongo
from pymongo import MongoClient
import pandas as pd
import csv
from datetime import datetime
import time
import  Mongo.mongo  as mongo

def Filter_out_device(DB,Collection,start_time,end_time):
    # 提取原始數據
    search_data = {"Datetime": {"$gte": start_time, "$lte": end_time}}
    raw_data =  mongo.WIFI_FindData(DB,Collection,search_data)
    print("ok")


    # 在 Python 中進行處理和判断，找到每个用户連接了不同 ap_identifier 種類數量最多的設備
    user_devices = {}

    for document in raw_data:
        # 或取用户名、設備 MAC 和 AP 標示符
        user_name = document.get("client_user_name", "")
        device_mac = document.get("sta_mac_address", "")
        ap_identifier = document.get("ap_name", "")

        # 檢查用户名中是否包含@，然后進行相應的處理
        if '@' in user_name:
            user_name = user_name.split('@')[0].lower()
        else:
            user_name = user_name.lower()

        if user_name and device_mac and ap_identifier:
            key = f"{user_name}_{device_mac}"
        if key not in user_devices:
            user_devices[key] = {"user_name": user_name, "device_mac": device_mac, "ap_identifiers": set()}
        user_devices[key]["ap_identifiers"].add(ap_identifier)
        
    # 找到每个用户連接了 ap_identifier 種類數量最多的設備
    top_devices = {}

    # 考慮同一用户可能只有一個設備的情况
    for key, data in user_devices.items():
        user_name = data["user_name"]
        if user_name not in top_devices:
            top_devices[user_name] = [data]
        else:
            top_devices[user_name].append(data)


    # 找到每个用户連接了不同 ap_identifier 種類數量最多的設備
    final_top_devices = []

    for user_name, devices in top_devices.items():
        devices.sort(key=lambda x: len(x["ap_identifiers"]), reverse=True)
        top_device = devices[0]
        final_top_devices.append({
            "user_name": top_device["user_name"],
            "device_mac": top_device["device_mac"],
            "ap_identifiers_count": len(top_device["ap_identifiers"])
        })

    # 打印最终结果
    #for device in final_top_devices:
        #print(device)
    #mongo.WIFI_WriteInDB("AP_test","MACaddress_test3" , final_top_devices )

    

    #創建一个集合来存储要保留的設備 MAC 地址
    set_of_device_macs_to_keep = set()

    # 填充要保留的設備 MAC 地址集合
    for top_device in final_top_devices:
        set_of_device_macs_to_keep.add(top_device["device_mac"])

    # 創建一個列表来存储要插入新數據庫的文檔
    documents_to_insert = []

    for document in raw_data:
        # 獲取設備 MAC
        device_mac = document.get("sta_mac_address", "")

        # 檢查是否需要保留此設備
        if device_mac in set_of_device_macs_to_keep:
            # 將此文檔添加到要插入的文檔列表中
            documents_to_insert.append(document)
   # print(documents_to_insert)
    documents_to_insert.append(final_top_devices)
    return documents_to_insert
    # 插入要保留的文檔到新的數據庫
    #mongo.WIFI_WriteInDB("AP_test","MACaddress_test4" , documents_to_insert )



