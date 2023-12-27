import sys
from bson import ObjectId
import pymongo
from pymongo import MongoClient
import pandas as pd
import csv
import os
from datetime import datetime
import time
from dotenv import load_dotenv
load_dotenv()
mongo_url_01=os.getenv('MongoClient')
mongo_url_02=os.getenv('MongoClient')



def WIFI_LastData(DB, Collection):# Search last Data
    global mongo_url_01, mongo_url_02
    try:
        conn = MongoClient(mongo_url_01)
        db = conn[DB]
        collection = db[Collection]
        cursor = collection.find().sort("_id", -1).limit(1)
        data = [d for d in cursor]
    except:
        conn = MongoClient(mongo_url_02)
        db = conn[DB]
        collection = db[Collection]
        cursor = collection.find().sort("_id", -1).limit(1)
        data = [d for d in cursor]
    if data == []:
        return False
    else:
        return data


def WIFI_FindData(DB, Collection, Search):# According "Search" to search data
    global mongo_url_01, mongo_url_02
    try:
        conn = MongoClient(mongo_url_01)
        db = conn[DB]
        collection = db[Collection]
        cursor = collection.find(Search)
        data = [d for d in cursor]
    except:
        data=False
    if data == []:
        return False
    else:
        return data

def WIFI_WriteInDB(DB, Collection, new_data):# Write many data in DB
    global mongo_url_01, mongo_url_02
    try:
        conn = MongoClient(mongo_url_01)
        db = conn[DB]
        collection = db[Collection]
        collection.insert_many(new_data)
    except:

        conn = MongoClient(mongo_url_02)
        db = conn[DB]
        collection = db[Collection]
        collection.insert_many(new_data)
def WIFI_WriteInDB_one(DB, Collection, new_data):# Write One data in DB
    global mongo_url_01, mongo_url_02
    try:
        conn = MongoClient(mongo_url_01)
        db = conn[DB]
        collection = db[Collection]
        collection.insert_one(new_data)
    except:

        conn = MongoClient(mongo_url_02)
        db = conn[DB]
        collection = db[Collection]
        collection.insert_one(new_data)

def WIFI_DelData(DB, Collection, document_id):#Delet one Data according document_id
    global mongo_url_01, mongo_url_02
    try:
        conn = MongoClient(mongo_url_01)
        db = conn[DB]
        collection = db[Collection]
        collection.find_one_and_delete({'_id': ObjectId(document_id)})
    except:
        conn = MongoClient(mongo_url_02)
        db = conn[DB]
        collection = db[Collection]
        collection.find_one_and_delete({'_id': ObjectId(document_id)})

    
def WIFI_CheckData(DB, Collection):#Confirm whether there is data in DB
    global mongo_url_01,mongo_url_02
    try:
            conn = MongoClient(mongo_url_01) 
            db = conn[DB]
            collection = db[Collection]
           
    except:
            conn = MongoClient(mongo_url_02) 
            db = conn[DB]
            collection = db[Collection]
    if collection.count_documents({}) == 0:
       return 0
    else:
       return 1
