from logger.kafkaLogger import KafkaLogger
from conf.configManager import ConfigManager
from migration.migration import Migration



logger = KafkaLogger()
parser = ConfigManager()

conf = parser.readConfig()


migration = Migration(conf)
try:
    migration.preExperiment()
    migration.runExperiment()
    migration.postExperiment()
finally:
    logger.terminate_kafka_logger()
