import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://admin:admin123@mongo:27017"

print(f"=== Connecting to MongoDB using URI: {mongo_uri}")

client = MongoClient(mongo_uri)
db = client.audit_db
collection = db["audit"]
