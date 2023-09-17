import pandas as pd
import requests
import warnings
import time
from bs4 import BeautifulSoup
import json
import os
import datetime
import numpy as np
import pymongo
from pymongo import MongoClient
import re
import arubaapi
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from datetime import timedelta
import os
from dotenv import load_dotenv

def start_Controller_249_Client():
    load_dotenv()
    start_time = time.time()
    # =============================================================================

    ################################ CLIENT DATA ##################################

    # =============================================================================
    # MongoDB Database & Collection

    # Database="Client"
    # Collections="Controller4"


    # =============================================================================

    # Aruba API account & password

    account = os.getenv('Controller_249_account')
    password = os.getenv('Controller_249_password')


    # =============================================================================

    # enter Aruba API Controller dashboard url

    Controller_url = os.getenv('Controller_249_url')
    # =============================================================================

    # auto login and get cookie

    url = Controller_url+'/screens/wms/wms.login'
    headers = {'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    chartData = 'opcode=login&url=%2Flogin.html&needxml=0&uid='+account+'&passwd='+password
    res_data = requests.post(
        url, verify=False, headers=headers, data=chartData.encode('utf-8'))
    cookieStr = res_data.cookies['SESSION']


    # =============================================================================

    # Retrieve and parse AP data

    url = Controller_url+'/screens/cmnutil/execUiQuery.xml'
    headers = {'Content-Type': 'text/plain'}
    cookie = {"SESSION": cookieStr}
    payloadData = 'query=<aruba_queries><query><qname>backend-observer-sta-21</qname><type>list</type><list_query><device_type>sta</device_type><requested_columns>sta_mac_address client_ip_address client_user_name client_role_name client_health ssid ap_name channel channel_str radio_band bssid speed snr total_data_bytes avg_data_rate tx_bytes_transmitted rx_data_bytes total_data_throughput</requested_columns><pagination><start_row>0</start_row><num_rows>5000</num_rows></pagination></list_query><filter><global_operator>and</global_operator><filter_list><filter_item_entry><field_name>client_conn_type</field_name><comp_operator>not_equals</comp_operator><value><![CDATA[0]]></value></filter_item_entry></filter_list></filter></query></aruba_queries>&UIDARUBA='+cookieStr
    res = requests.post(url, verify=False, headers=headers,
                        cookies=cookie, data=payloadData.encode('utf-8'))
    soup = BeautifulSoup(res.text, 'html.parser')
    header_tags = soup.find_all('header')
    row_tags = soup.find_all('row')


    # =============================================================================

    # Rearrange DataFrame: put into df[]

    df = pd.DataFrame()
    index = 0
    for values in row_tags:

        data = values.find_all('value')
        data_total = []

        time_stamp = int(time.time())
        struct_time = time.localtime(time_stamp)
        timeString = time.strftime("%Y-%m-%d-%H-%M", struct_time)
        data_total.append(time_stamp)

        for i in range(len(data)):

            data_total.append(data[i].text)

        index += 1
        df[index] = data_total

    for values in header_tags:
        Client_Data = []
        Client_Data.append('time_stamp')
        column_name = values.find_all('column_name')
        for i in range(len(column_name)):
            Client_Data.append(column_name[i].text)

    df.index = Client_Data
    df = df.T
    df = df.sort_values(by=['ap_name'])
    df.reset_index(drop=True, inplace=True)

    # =============================================================================

    # Add datetime (GMT +8) and timestamp: put into df[]

    for i in range(len(df)-1):
        try:
            df['time_stamp'][i] = int(df[i]['time_stamp'][i])
        except Exception:
            df['time_stamp'][i] = 0
        try:
            df['client_health'][i] = int(df['client_health'][i])
        except Exception:
            df['client_health'][i] = 0
        try:
            df['radio_band'][i] = int(df['radio_band'][i])
        except Exception:
            df['radio_band'][i] = 0
        try:
            df['speed'][i] = int(df['speed'][i])
        except Exception:
            df['speed'][i] = 0
        try:
            df['snr'][i] = int(df['snr'][i])
        except Exception:
            df['snr'][i] = 0
        try:
            df['total_data_bytes'][i] = int(df['total_data_bytes'][i])
        except Exception:
            df['total_data_bytes'][i] = 0
        try:
            df['avg_data_rate'][i] = int(df['avg_data_rate'][i])
        except Exception:
            df['avg_data_rate'][i] = 0
        try:
            df['tx_bytes_transmitted'][i] = int(df['tx_bytes_transmitted'][i])
        except Exception:
            df['tx_bytes_transmitted'][i] = 0
        try:
            df['rx_data_bytes'][i] = int(df['rx_data_bytes'][i])
        except Exception:
            df['rx_data_bytes'][i] = 0
        try:
            df['total_data_throughput'][i] = int(df['total_data_throughput'][i])
        except Exception:
            df['total_data_throughput'][i] = 0

    # =============================================================================

    # Add datetime (GMT +8) and timestamp: put into df[]


    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    ts = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fz")
    ts
    n = 8
    # Subtract 8 hours from datetime object
    ts = ts - timedelta(hours=n)
    ts_tw_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_tw = datetime.now()


    # =============================================================================

    # create json: df[] => data_json

    data_json3 = json.loads(df.to_json(orient='records'))


    # =============================================================================

    # Append ISODate

    for i in range(len(data_json3)):
        data_json3[i]['ts'] = ts
        data_json3[i]['DatetimeStr'] = ts_tw_str
        data_json3[i]['Datetime'] = ts_tw


    # =============================================================================

    # Store json data to MongoDB

    # select mongo address
    # select mongo database
    # select mongo collection in db
    # put the combined json data into db

    client = MongoClient(
        "mongodb://administrator:administrator@140.118.70.40:27017/")
    db1 = client['Client']
    col1 = db1["Controller4"]
    col1.insert_many(data_json3)

    db2 = client['Client']
    col2 = db2["may_data"]
    col2.insert_many(data_json3)

    end_time = time.time()
    total_time = end_time - start_time

    print('Client_data OK')
    print("total running period?%.2f?" % total_time)
