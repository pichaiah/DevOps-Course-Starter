import requests
import json
import os
from item import Item
import json
import pymongo
from bson import json_util 
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

headers = {
   "Accept": "application/json"
}

def get_db_name():  
    db_name = os.getenv('MONGO_DB_NAME') 
    if db_name is None:
        db_name = "Board"
    return db_name

def get_items_db_tablename():  
    items_table_name = os.getenv('ITEMS_TABLE_NAME') 
    if items_table_name is None:
        items_table_name = "Items"
    return items_table_name

def get_board_db():
    db_url = os.getenv('MONGO_DB_URL')
    if db_url is None:
        raise Exception("Environment variable MONGO_DB_URL is not set")
    print(f"Database URL: {db_url}")
    db_name = get_db_name()    
    client = MongoClient(db_url)
    db = client[db_name]
    return db

def get_all_items():       
    db = get_board_db()        
    card_collection_name = get_items_db_tablename()
    card_collection = db[card_collection_name]
    item_list = []
    for card in card_collection.find():            
        item_list.append(Item(id=card['_id'], status=card['Status'], title=card['Title'], last_modified=card['LastModified']))
    
    return item_list

def create_todo_item(title):
    db = get_board_db()
    card_collection_name = get_items_db_tablename()
    card_collection = db[card_collection_name]
    card = {
        "Title": title,
        "Status": "To Do",
        "LastModified":datetime.datetime.utcnow()
    }
    card_collection.insert_one(card)        

def move_to_doing(id):
    update_status(id, "Doing")

def move_to_done(id):    
    update_status(id, "Done")
   
def update_status(id, status):    
    db = get_board_db()
    card_collection_name = get_items_db_tablename()
    card_collection = db[card_collection_name]    
    id_filter = { "_id": ObjectId(id) }
    newvalues = { 
        "$set": {
             "Status": status,
             "LastModified":datetime.datetime.utcnow()}        
        }    
    card_collection.update(id_filter, newvalues, upsert=True)    


def delete_item(id):
    db = get_board_db()
    card_collection_name = get_items_db_tablename()
    card_collection = db[card_collection_name] 
    id_filter = { "_id": ObjectId(id) }
    card_collection.delete_one(id_filter)

def get_item(title):
    db = get_board_db()
    card_collection_name = get_items_db_tablename()
    card_collection = db[card_collection_name] 
    title_filter = { "Title": title }
    return card_collection.find_one(title_filter)
