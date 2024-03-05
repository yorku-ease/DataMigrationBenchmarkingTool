from confluent_kafka import Producer
import configparser
class KafkaLogger:
    _instance = None  # Private class variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KafkaLogger, cls).__new__(cls)
            cls._instance.init_kafka_logger(*args, **kwargs)
        return cls._instance

    def init_kafka_logger(self):
        # Define the Kafka broker(s) and topic name
        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  # Set the prefix character for comments
        config.read('configs/migrationEngineConfig.ini')

        kafkaClusterIP = config.get('KafkaCluster', 'host')
        kafkaClusterPort = config.get('KafkaCluster', 'port')
        self.bootstrap_servers = f"{kafkaClusterIP}:{kafkaClusterPort}"  
        self.performanceBenchmarkTopic = config.get('KafkaCluster', 'performanceBenchmarkTopic')  
        self.migrationEngineTopicName = config.get('KafkaCluster', 'migrationEngineTopicName')
        # Create a Kafka producer instance
        self.producer = Producer({
            'bootstrap.servers': self.bootstrap_servers,
            'acks': 'all',  # Wait for all in-sync replicas to acknowledge
            'delivery.timeout.ms': 10000  # Set a delivery timeout (optional)
        })

    def log(self,topic_name, id, message_value):
        self.producer.produce(topic=topic_name, key=id, value=message_value)
        
    def logPerformanceBenchmark(self,id, message_value):
        self.producer.produce(topic=self.performanceBenchmarkTopic, key=id, value=message_value)
          

    def logMigrationEngine(self,id, message_value):
        self.producer.produce(topic=self.migrationEngineTopicName, key=id, value=message_value)

    def terminate_kafka_logger(self):
        # Wait for any outstanding messages to be delivered and delivery reports to be received
        self.producer.flush()
