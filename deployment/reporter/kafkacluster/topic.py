from confluent_kafka.admin import AdminClient, NewTopic
import time

# Define the Kafka broker(s) and topic name
bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
topic_name = "my_topic"  # Replace with the desired topic name

# Create an AdminClient instance
admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

# Check if the topic already exists
existing_topics = admin_client.list_topics().topics.keys()

if topic_name in existing_topics:
    print(f"Topic '{topic_name}' already exists.")
else:
    # Create a new topic with the desired configuration
    new_topic = NewTopic(topic_name,1,1)

    # Create the topic
    admin_client.create_topics([new_topic])
    while topic_name not in existing_topics:
        print(f"Creating Topic ...")
        existing_topics = admin_client.list_topics().topics.keys()
        time.sleep(1)


    print(f"Topic '{topic_name}' created successfully.")
