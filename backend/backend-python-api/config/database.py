from pymongo import MongoClient

uri = "mongodb://localhost:27017/doan4_luuducquang_bida"
client = MongoClient(uri)
database = client.get_database()

role_collection = database['Roles']

role_collection.create_index([("role_name", 1)], unique=True)