import time
import logging
from confluent_kafka import Producer

# Setting Logger
logger = logging.getLogger("Producer Demo")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def read_config():
    """Reads client properties from a file."""
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config

def delivery_report(err, msg):
    """Callback for delivery reports."""
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def produce(topic, config):

    # Create the producer instance
    producer = Producer(config)

    try:
        for l in range(3):  # Outer loop
            for i in range(30):  # Inner loop
                key = f"id-{i}"
                value = f"World {i}!"
                
                # Serialize key and value during production
                producer.produce(
                    topic, 
                    key=key, 
                    value=value, 
                    callback=delivery_report
                )
                time.sleep(0.5)  # Delay between messages

        producer.flush()  # Ensure all messages are sent
    except Exception as e:
        logger.error(f"Error in producer: {e}")
    except KeyboardInterrupt:
        logger.info("Producer interrupted")
    finally:
        producer.flush()

def main():
    # config = read_config()
    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:19092',

        'acks': 'all'
    }
    topic = "topic_2"
    produce(topic, config)

if __name__ == "__main__":
    main()
