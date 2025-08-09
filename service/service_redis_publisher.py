from redis import Redis
from datetime import datetime

redis_client = Redis(host='localhost', port=6379,decode_responses=True)

def publish_to_redis(operation:str, event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()
    event["operation"] = operation

    redis_client.xadd("math_stream", event)