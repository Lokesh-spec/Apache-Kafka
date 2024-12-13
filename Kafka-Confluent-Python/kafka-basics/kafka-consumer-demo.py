import logging
from confluent_kafka import Consumer, KafkaError, KafkaException
from datetime import datetime

# Setting Logger
logger = logging.getLogger("Consumer Demo")
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

def consume(topic, config):
    config["group.id"] = "python-group-1"
    config["auto.offset.reset"] = "earliest"
    # config["partition.assignment.strategy"] = "sticky"
    consumer = Consumer(config)
    consumer.subscribe([topic])  # Dynamically subscribe to topic

    try:
        while True:
            msg = consumer.poll(timeout=5.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"End of partition {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
                continue
            value = msg.value().decode('utf-8')
            timestamp = datetime.fromtimestamp(msg.timestamp()[1] / 1000.0)
            logger.info(f"Received message: topic={msg.topic()}, partition={msg.partition()}, "
                        f"offset={msg.offset()}, timestamp={timestamp}, value={value}")
    except KeyboardInterrupt:
        logger.info("Consumer is starting to shut down")
    except Exception as e:
        logger.error(f"Error in consumer: {e}")
    finally:
        consumer.close()
        logger.info("The Consumer is now gracefully shut down!!")

def main():
    # config = read_config()
    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:19092',

        'acks': 'all'
    }
    topic = "topic_2"
    consume(topic, config)

if __name__ == "__main__":
    main()
