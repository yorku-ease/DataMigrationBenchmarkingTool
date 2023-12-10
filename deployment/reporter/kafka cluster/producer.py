from confluent_kafka import Producer

# Define the Kafka broker(s) and topic name
bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
topic_name = "my_topic"  # Replace with the Kafka topic you want to produce to

# Create a Kafka producer instance
producer = Producer({
    'bootstrap.servers': bootstrap_servers,
    'acks': 'all',  # Wait for all in-sync replicas to acknowledge
    'delivery.timeout.ms': 10000  # Set a delivery timeout (optional)
})

# Produce a message to the Kafka topic
message_key = "key1"  # Replace with your message key if needed
message_value = "Hello, Kafka!"  # Replace with your message content

producer.produce(topic=topic_name, key=message_key, value=message_value)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()


