from confluent_kafka import Producer

class KafkaLogger():
    def __init__(self):
                        # Define the Kafka broker(s) and topic name
        self.bootstrap_servers = "192.168.122.143:9092"  # Replace with your Kafka broker address
        self.topic_name = "my_topic"  # Replace with the Kafka topic you want to produce to

        # Create a Kafka producer instance
        self.producer = Producer({
            'bootstrap.servers': self.bootstrap_servers,
            'acks': 'all',  # Wait for all in-sync replicas to acknowledge
            'delivery.timeout.ms': 10000  # Set a delivery timeout (optional)
        })
    def log(self,id,message_value):

        self.producer.produce(topic=self.topic_name, key=id, value=message_value)

    def terminatekafkalogger(self):
        # Wait for any outstanding messages to be delivered and delivery reports to be received
        self.producer.flush()