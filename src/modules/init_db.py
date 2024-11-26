import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

test_user = {
  "email": "user@test.com",
  "name": "testuser",
  "password": "user1234",
  "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  "wishlists": {}
}

test_comment = {
    "product_name": "test_product",
    "email": "user@test.com",
    "comment": "this is a test comment",
    "commented_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

def initialize_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        users_collection = db["users"]
        if users_collection.count_documents({}) == 0:
            users_collection.insert_one(test_user)

        comments_collection = db["comments"]
        if comments_collection.count_documents({}) == 0:
            comments_collection.insert_one(test_user)
        
        print("Database initialized successfully!")
    except Exception as e:
        print("Error initializing the Database: ", e)

if __name__ == "__main__":
    initialize_database()