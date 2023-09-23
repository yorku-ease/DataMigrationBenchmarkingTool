from confluent_kafka import Consumer, KafkaError

# Define the Kafka broker(s), group ID, and topic name
bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
group_id = "my_consumer_group"  # Replace with your desired group ID
topic_name = "my_topic"  # Replace with the Kafka topic you want to consume from

# Create a Kafka consumer instance
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',  # Start from the beginning of the topic
    'enable.auto.commit': False  # Disable automatic offset commits
})

output_file = "output.log"

# Subscribe to the Kafka topic
consumer.subscribe([topic_name])
with open(output_file, "a") as file:
    try:
        while True:
            # Poll for new messages
            msg = consumer.poll(1.0)  # Adjust the timeout as needed

            if msg is None:
                continue
            if msg.error():
                # Handle any errors
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition: {msg.partition()}")
                else:
                    print(f"Error: {msg.error()}")
            else:
                key = msg.key().decode('utf-8')
                value = msg.value().decode('utf-8')


                message = 'Key={}, Value={}'.format(key, value)
                print(message)
                file.write(f"{message}\n")
                file.flush()  # Ensure the message is written immediately

    except KeyboardInterrupt:
        pass

    finally:
        # Close the Kafka consumer gracefully
        consumer.close()

