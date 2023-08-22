from pymongo import MongoClient

client = MongoClient("127.0.0.1:27017")

db = client["TikTok_result"]

# Access a collection
collection = db["informations"]
