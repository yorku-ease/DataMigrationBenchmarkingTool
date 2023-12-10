from confluent_kafka import Consumer, KafkaError, Producer
from confluent_kafka.admin import AdminClient, NewTopic
import time

# Define the Kafka broker(s), group ID, and topic name

bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
group_id = "my_consumer_group"  # Replace with your desired group ID
topic_names = ["performanceBenchmark","framework","migrationEngine"]  # Replace with the Kafka topic you want to consume from
#topic_name = "framework"  # Replace with the Kafka topic you want to consume from



def create_topics(bootstrap_servers):
    # Create an AdminClient instance
    admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})
    print("Establishing connection with kafka")
    # Check if the topic already exists
    existing_topics = admin_client.list_topics().topics.keys()
    print("Kafka is ready!")
    for topic_name in topic_names:
        if topic_name not in existing_topics:
            # Create a new topic with the desired configuration
            new_topic = NewTopic(topic_name,1,1)

            # Create the topic
            admin_client.create_topics([new_topic])
            while topic_name not in existing_topics:
                print(f"Creating Topic ...")
                existing_topics = admin_client.list_topics().topics.keys()
                time.sleep(1)


        print(f"Topic '{topic_name}' created.")



def startConsumer():

    # Create a Kafka consumer instance
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',  # Start from the beginning of the topic
        'enable.auto.commit': False  # Disable automatic offset commits
    })


    topic_files = {}
    for topic_name in topic_names:
        topic_files[topic_name] = open(f"{topic_name}.log","a")

    # Subscribe to the Kafka topic
    consumer.subscribe(topic_names)
    print(f"Consumer subscribed to topics and waiting for messages ...")
    
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
                topic = msg.topic()
                key = msg.key().decode('utf-8')
                value = msg.value().decode('utf-8')


                message = 'Key={}, Value={}'.format(key, value)
                print(message)
                topic_files[topic].write(f"{message}\n")
                topic_files[topic].flush()  # Ensure data is written immediately

    except KeyboardInterrupt:
        pass

    finally:
        # Close the Kafka consumer gracefully
        consumer.close()
        for file in topic_files.values():
            file.close()

    for file in topic_files.values():
        file.close()


create_topics(bootstrap_servers)
startConsumer()


