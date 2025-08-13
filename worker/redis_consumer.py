import redis
import json

from datetime import datetime
from pymongo import collection
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def run_consumer():
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
    last_id = "0-0"  # Start at the beginning, or use "$" for only new messages

    log.info("🛰️  Listening to Redis stream 'math_api_stream'...")

    while True:
        response = redis_client.xread({"math_api_stream": last_id}, block=0, count=1)

        if response:
            stream, messages = response[0]
            for message_id, data in messages:
                log.info(f"\n📨 [Message ID: {message_id}] Received:")
                log.info(json.dumps(data, indent=2))

                try:
                    operation = data.get("operation")
                    payload = json.loads(data.get("payload", "{}"))
                    timestamp = data.get("timestamp")

                    # Save to MongoDB
                    collection.insert_one({
                        "operation": operation,
                        "request": payload,
                        "timestamp": datetime.fromisoformat(timestamp)
                    })
                    log.info("Logged to MongoDB")
                except Exception as e:
                    log.error(f"Error processing message: {e}")

                last_id = message_id  # Move to next message

if __name__ == "__main__":
    run_consumer()
