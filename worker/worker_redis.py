from redis import Redis

import logging

# Configure the logging
logging.basicConfig(level=logging.INFO)

client = Redis(host='redis', port=6379, decode_responses=True)


def main():
    stream = "math_stream"
    group = "math_group"
    consumer = "math_consumer"

    try:
        client.xgroup_create(stream, group, id='0', mkstream=True)
    except:
        pass

    while True:
        response = client.xreadgroup(
            group,
            consumer,
            {stream: ">"},
            count=1,
            block=2000
        )

        if response:
            stream, messages = response[0]
            message_id, message_data = messages[0]
            logging.info(f"Received message '{message_id}': {message_data}")

            client.xack(stream, group, message_id)
            logging.info(f"Message '{message_id}' acknowledged.")


if __name__ == "__main__":
    main()
