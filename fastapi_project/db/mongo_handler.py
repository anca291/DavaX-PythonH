from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["math_service"]
collection = db["requests"]

def log_math_operation(operation: str, request: dict, result: float):
    entry = {
        "operation": operation,
        "request": request,
        "result": result,
        "timestamp": datetime.datetime.utcnow()
    }
    collection.insert_one(entry)

def get_recent_requests(limit: int = 10):
    return list(collection.find().sort("timestamp", -1).limit(limit))
