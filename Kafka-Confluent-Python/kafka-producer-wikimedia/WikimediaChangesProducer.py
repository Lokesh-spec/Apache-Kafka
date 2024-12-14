import time
import logging
from confluent_kafka import Producer

from WikimediaChangeHandler import WikimediaChangeHandler


logger = logging.getLogger("Wikimedia Changes Producer")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class WikimediaChangesProducer:
    
    def __init__(self, topic, config, url):
        self.kafka_producer = Producer(config)
        self.topic = topic
        self.url = url
        
        
    def wikimedia_change_handler(self):
        change_handler = WikimediaChangeHandler(self.kafka_producer, self.topic, self.url)
        
        try:
            logger.info("Start consuming events from Wikimedia stream")
            change_handler.handle_stream()
        except KeyboardInterrupt:
            logger.info("Stream processing stopped by user.")
        except Exception as e:
            logger.info(f"Exception in handling stream! - {e}")
        finally:
            # Close the Kafka producer
            self.kafka_producer.flush()
            logger.info("Kafka producer closed.")
        
if __name__ == "__main__":
    
    topic = "wikimedia.recentchange"
    
    config = {
        'bootstrap.servers': 'localhost:19092',
        'linger.ms' : '20',
        'compression.type' : 'snappy',
        'batch.size' : 32 * 1024
   }
    
    url = "https://stream.wikimedia.org/v2/stream/recentchange"
    
    wikimedia_changes_producer = WikimediaChangesProducer(topic, config, url)
    
    wikimedia_changes_producer.wikimedia_change_handler()