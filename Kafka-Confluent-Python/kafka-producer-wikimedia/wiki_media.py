import requests

url = "https://stream.wikimedia.org/v2/stream/recentchange"


with requests.get(url, stream=True) as response:
    if response.status_code != 200:
        print(f"Failed to connect to the stream, status code {response.status_code}")

    # Iterate through the response line by line
    for line in response.iter_lines():
        if line:
            try:
                # Decode the line to a string and check if it's a valid SSE message
                message_data = line.decode('utf-8')

                # Log the raw message (can be useful for debugging)
                print(f"Received message: {message_data}")

                # Send the message data to Kafka (assumed to be a simple string here)
                print(message_data)

            except Exception as e:
                print(f"Error processing line: {str(e)}")