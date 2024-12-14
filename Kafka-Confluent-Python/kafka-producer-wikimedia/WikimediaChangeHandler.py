import logging
import requests

logger = logging.getLogger("Wikimedia Change Handler")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class WikimediaChangeHandler:
    
    def __init__(self, kafka_producer, topic, url):
        self.kafka_producer = kafka_producer
        self.topic = topic
        self.url = url
        

    def send_to_kafka(self, message):
        try:
            self.kafka_producer.produce(self.topic, key=None, value=message)
            self.kafka_producer.flush()  
            logger.info(f"Message sent to Kafka: {message}")
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {str(e)}")
    
    
    def handle_stream(self):
        try:
            # Connect to the Wikimedia SSE stream using 'requests'
            logger.info("Connecting to Wikimedia stream...")

            # Start the GET request to stream data
            with requests.get(self.url, stream=True) as response:
                if response.status_code != 200:
                    logger.error(f"Failed to connect to the stream, status code {response.status_code}")
                    return
                else:
                    logger.info(f"Successfully conneted to the stream, status code {response.status_code}")

                # Iterate through the response line by line
                for line in response.iter_lines():
                    if line:
                        try:
                            # Decode the line to a string and check if it's a valid SSE message
                            message_data = line.decode('utf-8')

                            # Log the raw message (can be useful for debugging)
                            logger.info(f"Received message: {message_data}")

                            # Send the message data to Kafka (assumed to be a simple string here)
                            self.send_to_kafka(message_data)

                        except Exception as e:
                            logger.error(f"Error processing line: {str(e)}")

        except requests.RequestException as e:
            logger.error(f"Error connecting to Wikimedia stream: {str(e)}")