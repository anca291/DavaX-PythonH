import redis
import json
from datetime import datetime

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def stream_log(operation: str, data: dict):
    entry = {
        "operation": operation,
        "payload": json.dumps(data),
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.xadd("math_api_stream", entry)
