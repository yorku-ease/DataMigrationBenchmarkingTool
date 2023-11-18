from DefaultFileMigrator import DefaultFileMigrator
from KafkaLogger import KafkaLogger

import os,configparser

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)


config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('configs/migrationEngineConfig.ini')



remoteHostname = config.get('targetServer', 'host')
remoteUsername = config.get('targetServer', 'username')
remotePassword = config.get('targetServer', 'password')
localPassword = config.get('sourceServer', 'password')
loggingId = config.get('experiment', 'loggingId')
local_file_name = config.get('experiment', 'file')
local_file_path = config.get('sourceServer', 'dataFolder_path') + local_file_name
remote_file_path = config.get('targetServer', 'dataFolder_path') + local_file_name
compressionType = config.get('experiment', 'compressionType')
limit = int(config.get('experiment', 'limit'))
streams = int(config.get('experiment', 'streams'))


logger = KafkaLogger()


migrationEngine = DefaultFileMigrator(remoteHostname,remoteUsername,remotePassword,localPassword,loggingId,logger)
migrationEngine.migrate(local_file_path,remote_file_path,compressionType,limit,streams)

logger.terminate_kafka_logger()