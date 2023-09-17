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

def start_Controller_249_AP():
    load_dotenv()
    start_time = time.time()
    # =============================================================================

    ################################ AP DATA ######################################
    #                         (Add into RADIO DATA)
    # =============================================================================

    # MongoDB Database & Collection

    # Database="AP"
    # Collections="Controller4"


    # =============================================================================

    # Aruba API account & password

    account = os.getenv('Controller_249_account')
    password = os.getenv('Controller_249_password')


    # =============================================================================

    # enter Aruba API Controller dashboard url

    Controller_url = os.getenv('Controller_249_url')

    # Avoid warning

    warnings.filterwarnings('ignore')
    path = 'data.txt'


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

    # inspect => Network => payload => find execUiQuery.xml payload data that you need => put into the payload_data: 'whole string' + cookieStr

    url = Controller_url+'/screens/cmnutil/execUiQuery.xml'
    headers = {'Content-Type': 'text/plain'}
    cookie = {"SESSION": cookieStr}
    payloadData = 'query=<aruba_queries><query><qname>backend-observer-ap-9</qname><type>list</type><list_query><device_type>ap</device_type><requested_columns>ap_name ap_group ap_tri_radio_mode sta_count ap_ip_address</requested_columns><sort_by_field>ap_name</sort_by_field><sort_order>desc</sort_order><pagination><start_row>0</start_row><num_rows>1000</num_rows></pagination></list_query><filter><global_operator>and</global_operator><filter_list><filter_item_entry><field_name>ap_status</field_name><comp_operator>equals</comp_operator><value><![CDATA[1]]></value></filter_item_entry><filter_item_entry><field_name>role</field_name><comp_operator>equals</comp_operator><value><![CDATA[1]]></value></filter_item_entry></filter_list></filter></query></aruba_queries>&UIDARUBA='+cookieStr

    res = requests.post(url, verify=False, headers=headers,
                        cookies=cookie, data=payloadData.encode('utf-8'))

    soup = BeautifulSoup(res.text, 'html.parser')
    header_tags = soup.find_all('header')
    row_tags = soup.find_all('row')


    # =============================================================================

    # Rearrange DataFrame: put it into df[]

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


    # =============================================================================

    # Add header to dataframe: put it into df[]

    for values in header_tags:
        Header_Data = []
        Header_Data.append('time_stamp')
        column_name = values.find_all('column_name')
        for i in range(len(column_name)):
            Header_Data.append(column_name[i].text)


    df.index = Header_Data
    df = df.T
    df.reset_index(drop=True, inplace=True)


    # =============================================================================

    # Add datetime (GMT +8) and timestamp

    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    ts = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fz")
    ts
    n = 8

    # Subtract 8 hours from datetime object

    ts = ts - timedelta(hours=n)
    ts_tw_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_tw = datetime.now()


    # =============================================================================

    # create json: df[] => data_json2

    data_json2 = json.loads(df.to_json(orient='records'))


    # =============================================================================

    # data type transfer: str => int

    for i in range(len(data_json2)):
        try:
            data_json2[i]['sta_count'] = int(data_json2[i]['sta_count'])
            data_json2[i]['ap_tri_radio_mode'] = int(
                data_json2[i]['ap_tri_radio_mode'])
        except Exception:
            pass
        data_json2[i]['ts'] = ts
        data_json2[i]['DatetimeStr'] = ts_tw_str
        data_json2[i]['Datetime'] = ts_tw


    # =============================================================================

    ################################ RADIO DATA ###############################

    # =============================================================================

    # MongoDB Database & Collection

    # Database="AP"
    # Collections="Controller_4"


    # =============================================================================

    # Aruba API account & password

    account = os.getenv('Controller_249_account')
    password = os.getenv('Controller_249_password')


    # =============================================================================

    # enter Aruba API Controller dashboard url

    Controller_url = os.getenv('Controller_249_url')

    # Avoid warning

    warnings.filterwarnings('ignore')
    path = 'data.txt'


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
    payloadData = 'query=<aruba_queries><query><qname>backend-observer-radio-65</qname><type>list</type><list_query><device_type>radio</device_type><requested_columns>ap_name radio_band channel_str radio_mode total_data_bytes rx_data_bytes eirp_10x max_eirp noise_floor arm_ch_qual sta_count current_channel_utilization rx_time tx_time channel_interference channel_free channel_busy avg_data_rate tx_avg_data_rate rx_avg_data_rate ap_quality</requested_columns><sort_by_field>ap_name</sort_by_field><sort_order>asc</sort_order><pagination><start_row>0</start_row><num_rows>2000</num_rows></pagination></list_query></query></aruba_queries>&UIDARUBA='+cookieStr

    res = requests.post(url, verify=False, headers=headers,
                        cookies=cookie, data=payloadData.encode('utf-8'))

    soup = BeautifulSoup(res.text, 'html.parser')
    header_tags = soup.find_all('header')
    row_tags = soup.find_all('row')


    # =============================================================================

    # Rearrange DataFrame: put into df[]

    df = pd.DataFrame()
    index = 0

    row_tags[0]
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


    # =============================================================================

    # Add header to dataframe: put into df[]

    for values in header_tags:
        AP1_Data = []
        AP1_Data.append('time_stamp')
        column_name = values.find_all('column_name')
        for i in range(len(column_name)):
            AP1_Data.append(column_name[i].text)

    df.index = AP1_Data
    df = df.T
    df.reset_index(drop=True, inplace=True)


    # ===================================================================================

    # when 'noise_floor' is null, decide whether it should crawl the specific data again

    # def function recall(i): detect that [noise_floor][i] is missing, crawl the missing data again
    # recall(i) return df_2, which put all accurate data in it

    def recall(i):
        global account, password, Controller_url
        try:
            url = Controller_url+'/screens/wms/wms.login'
            headers = {'Content-Type': 'text/html',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            chartData = 'opcode=login&url=%2Flogin.html&needxml=0&uid='+account+'&passwd='+password
            res_data = requests.post(
                url, verify=False, headers=headers, data=chartData.encode('utf-8'))
            cookieStr = res_data.cookies['SESSION']
            url = Controller_url+'/screens/cmnutil/execUiQuery.xml'
            headers = {'Content-Type': 'text/plain'}
            cookie = {"SESSION": cookieStr}
            payloadData = 'query=<aruba_queries><query><qname>backend-observer-radio-65</qname><type>list</type><list_query><device_type>radio</device_type><requested_columns>ap_name radio_band channel_str radio_mode total_data_bytes rx_data_bytes eirp_10x max_eirp noise_floor arm_ch_qual sta_count current_channel_utilization rx_time tx_time channel_interference channel_free channel_busy avg_data_rate tx_avg_data_rate rx_avg_data_rate ap_quality</requested_columns><sort_by_field>ap_name</sort_by_field><sort_order>asc</sort_order><pagination><start_row>' + \
                str(i) + '</start_row><num_rows>1</num_rows></pagination></list_query></query></aruba_queries>&UIDARUBA='+cookieStr
            res = requests.post(url, verify=False, headers=headers,
                                cookies=cookie, data=payloadData.encode('utf-8'))
            soup = BeautifulSoup(res.text, 'html.parser')
            header_tags = soup.find_all('header')
            row_tags = soup.find_all('row')

            df_2 = pd.DataFrame()
            index = 0
            print(df_2)

            for values in row_tags:
                data = values.find_all('value')
                data_total = []
                time_stamp = int(time.time())
                struct_time = time.localtime(time_stamp)
                timeString = time.strftime("%Y-%m-%d-%H-%M", struct_time)
                data_total.append(time_stamp)

                for j in range(len(data)):
                    data_total.append(data[j].text)
                df_2[index] = data_total

            for values in header_tags:
                AP2_Data = []
                AP2_Data.append('time_stamp')
                column_name = values.find_all('column_name')
                for i in range(len(column_name)):
                    AP2_Data.append(column_name[i].text)

            df_2.index = AP2_Data
            df_2 = df_2.T
            df_2.reset_index(drop=True, inplace=True)

            return df_2
        except:
            print('error')
            df_2 = pd.DataFrame()
            return df_2

    # put df_2 into the original data array df, substitute the error data


    for i in range(len(df)):
        f = 0
        while (df['noise_floor'][i] == '' and f <= 2):
            f = f+1
            df_2 = recall(i)

            if (not df_2.empty):
                df['time_stamp'][i] = df_2['time_stamp'][0]
                df['noise_floor'][i] = df_2['noise_floor'][0]
                df['ap_name'][i] = df_2['ap_name'][0]
                df['radio_band'][i] = df_2['radio_band'][0]
                df['total_data_bytes'][i] = df_2['total_data_bytes'][0]
                df['avg_data_rate'][i] = df_2['avg_data_rate'][0]
                df['tx_avg_data_rate'][i] = df_2['tx_avg_data_rate'][0]
                df['rx_avg_data_rate'][i] = df_2['rx_avg_data_rate'][0]
                df['channel_str'][i] = df_2['channel_str'][0]
                df['radio_mode'][i] = df_2['radio_mode'][0]
                df['eirp_10x'][i] = df_2['eirp_10x'][0]
                df['max_eirp'][i] = df_2['max_eirp'][0]
                df['arm_ch_qual'][i] = df_2['arm_ch_qual'][0]
                df['sta_count'][i] = df_2['sta_count'][0]
                df['current_channel_utilization'][i] = df_2['current_channel_utilization'][0]
                df['rx_time'][i] = df_2['rx_time'][0]
                df['tx_time'][i] = df_2['tx_time'][0]
                df['channel_interference'][i] = df_2['channel_interference'][0]
                df['channel_free'][i] = df_2['channel_free'][0]
                df['channel_busy'][i] = df_2['channel_busy'][0]

    # =============================================================================

    # data type transfer: str => int, xxxx/60000 => decimal point

    df['sta_count_all'] = df['sta_count']
    for i in range(len(df)):
        try:
            df['tx_time'][i] = int(re.findall(
                "([0-9]+)\/", df['tx_time'][i])[0])
        except Exception:
            df['tx_time'][i] = 0
        try:
            df['rx_time'][i] = int(re.findall(
                "([0-9]+)\/", df['rx_time'][i])[0])
        except Exception:
            df['rx_time'][i] = 0
        try:
            df['channel_interference'][i] = int(re.findall(
                "([0-9]+)\/", df['channel_interference'][i])[0])
        except Exception:
            df['channel_interference'][i] = 0
        try:
            df['channel_free'][i] = int(re.findall(
                "([0-9]+)\/", df['channel_free'][i])[0])
        except Exception:
            df['channel_free'][i] = 0
        try:
            df['channel_busy'][i] = int(re.findall(
                "([0-9]+)\/", df['channel_busy'][i])[0])/60000
        except Exception:
            df['channel_busy'][i] = 0
        try:
            df['total_data_bytes'][i] = int(df['total_data_bytes'][i])
        except Exception:
            df['total_data_bytes'][i] = 0
        try:
            df['rx_data_bytes'][i] = int(df['rx_data_bytes'][i])
        except Exception:
            df['rx_data_bytes'][i] = 0
        try:
            df['noise_floor'][i] = int(df['noise_floor'][i])
        except Exception:
            df['noise_floor'][i] = 0
        try:
            df['eirp_10x'][i] = int(df['eirp_10x'][i])
        except Exception:
            df['eirp_10x'][i] = 0
        try:
            df['max_eirp'][i] = int(df['max_eirp'][i])
        except Exception:
            df['max_eirp'][i] = 0
        try:
            df['arm_ch_qual'][i] = int(df['arm_ch_qual'][i])
        except Exception:
            df['arm_ch_qual'][i] = 0
        try:
            df['sta_count'][i] = int(df['sta_count'][i])
        except Exception:
            df['sta_count'][i] = 0
        try:
            df['avg_data_rate'][i] = int(df['avg_data_rate'][i])
        except Exception:
            df['avg_data_rate'][i] = 0
        try:
            df['tx_avg_data_rate'][i] = int(df['tx_avg_data_rate'][i])
        except Exception:
            df['tx_avg_data_rate'][i] = 0
        try:
            df['rx_avg_data_rate'][i] = int(df['rx_avg_data_rate'][i])
        except Exception:
            df['rx_avg_data_rate'][i] = 0
        try:
            df['ap_quality'][i] = int(df['ap_quality'][i])
        except Exception:
            df['ap_quality'][i] = 0
        try:
            df['radio_mode'][i] = int(df['radio_mode'][i])
        except Exception:
            df['radio_mode'][i] = 0

    # Add total client number

        for i in range(len(df) - 1):
            if df['ap_name'][i] == df['ap_name'][i+1]:
                df['sta_count_all'][i] = int(
                    df['sta_count'][i]) + int(df['sta_count'][i+1])
                df['sta_count_all'][i+1] = df['sta_count_all'][i]


    # =============================================================================

    # Add datetime (GMT +8) and timestamp


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

    data_json = json.loads(df.to_json(orient='records'))

    for i in range(len(data_json)):
        data_json[i]['ts'] = ts
        data_json[i]['DatetimeStr'] = ts_tw_str
        data_json[i]['Datetime'] = ts_tw

        # transfer all chanel_utilization data into percentage
        try:
            data_json[i]['rx_time_percent'] = data_json[i]['rx_time']/60000
        except Exception:
            data_json[i]['rx_time_percent'] = 0
        try:
            data_json[i]['tx_time_percent'] = data_json[i]['tx_time']/60000
        except Exception:
            data_json[i]['tx_time_percent'] = 0
        try:
            data_json[i]['channel_interference_percent'] = data_json[i]['channel_interference']/60000
        except Exception:
            data_json[i]['channel_interference_percent'] = 0
        try:
            data_json[i]['channel_free_percent'] = data_json[i]['channel_free']/60000
        except Exception:
            data_json[i]['channel_free_percent'] = 0

        # count tx_data_bytes
        data_json[i]['tx_data_bytes'] = data_json[i]['total_data_bytes'] - \
            data_json[i]['rx_data_bytes']

        # decide whether radio_band is 0 or 1, and add 2.4G and 5G tag

        if (data_json[i]['radio_band'] == "1"):
            data_json[i]['channel_Hz'] = 5
        else:
            data_json[i]['channel_Hz'] = 2.4

        ap_group_building = data_json[i]['ap_name'].split("_")
        data_json[i]['ap_group_building'] = ap_group_building[0]
        ap_group_floor = data_json[i]['ap_name'].split("_")
        data_json[i]['ap_group_floor'] = ap_group_building[1]
        ap_group_name = data_json[i]['ap_name'].split("_")
        data_json[i]['ap_group_name'] = ap_group_name[2]

        if (ap_group_building[0] == "TR" and ap_group_building[1] == "CR"):

            data_json[i]['ap_group_building'] = ap_group_building[0] + \
                '_' + ap_group_building[1]
            ap_group_floor = data_json[i]['ap_name'].split("_")
            data_json[i]['ap_group_floor'] = ap_group_building[2]
            ap_group_name = data_json[i]['ap_name'].split("_")
            data_json[i]['ap_group_name'] = ap_group_name[3]


    # =============================================================================

    # combine data from AP to RADIO
    # sort AP data to RADIO data with same AP name ==> if same ap name, data_json2(AP) put into data_json(RADIO)

    for i in range(len(data_json)):
        for j in range(len(data_json2)):
            if (data_json[i]['ap_name'] == data_json2[j]['ap_name']):
                data_json[i]['ap_group'] = data_json2[j]['ap_group']
                data_json[i]['ap_tri_radio_mode'] = data_json2[j]['ap_tri_radio_mode']
                data_json[i]['ap_ip_address'] = data_json2[j]['ap_ip_address']
                break


    # =============================================================================

    # Store json data to MongoDB


    previous_day = datetime.now() - timedelta(days=1)

    # select mongo address
    # select mongo database
    # select mongo collection in db
    # put the combined json data into db
    MongoClient_data=os.getenv('MongoClient')
    client = MongoClient(MongoClient_data)
    db1 = client['AP']
    col1 = db1["Controller4"]
    col1.insert_many(data_json)

    db2 = client['AP']
    col2 = db2["may_data"]
    col2.insert_many(data_json)

    end_time = time.time()
    total_time = end_time - start_time


    print('AP_data OK')
    print("total running period?%.2f?" % total_time)

