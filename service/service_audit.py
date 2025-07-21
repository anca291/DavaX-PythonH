import datetime

from config.database import collection


async def log_math_operation(operation: str, request: dict):
    entry = {
        "operation": operation,
        "request": request,
        "timestamp": datetime.datetime.utcnow()
    }
    collection.insert_one(entry)


def get_recent_requests(limit: int = 10):
    return list(collection.find().sort("timestamp", -1).limit(limit))
