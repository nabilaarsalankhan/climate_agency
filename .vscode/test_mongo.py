# E:\python_django\Climate_Agency\climate_data\test_mongo.py

from pymongo import MongoClient

def test_mongo_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db_list = client.list_database_names()
        print("✅ MongoDB Connection Successful!")
        print("Databases:", db_list)
    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)
