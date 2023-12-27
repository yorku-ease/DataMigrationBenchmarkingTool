import time,os,configparser
from classes.Experiment import Experiment
from classes.KafkaLogger import KafkaLogger
from itertools import product


# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

logger = KafkaLogger()

timeBeforeExperiment = time.time()

config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('configs/config.ini')




localPassword  = config.get('sourceServer', 'password')

remoteHostname = config.get('targetServer', 'host')
remoteUsername = config.get('targetServer', 'username')
remotePassword = config.get('targetServer', 'password')




#Total tranfer time must always be calculated here

numberOfExperiments = config.getint('migrationEnvironment', 'numberOfExperiments')
cloggingId = config.get('migrationEnvironment', 'loggingId')


experimentLists = dict(config['experiment'])
experimentLists = {key: value.split(',') if ',' in value else [value] for key, value in experimentLists.items()}

# Generate all combinations
experimentsCombinations = list(product(*experimentLists.values()))

# Create a list of dictionaries with combinations
experimentsCombinations = [dict(zip(experimentLists.keys(), combination)) for combination in experimentsCombinations]


try:
    for experimentOptions in experimentsCombinations:
        startTime = str(time.time())
        for i in range(0,numberOfExperiments):
            if not cloggingId:
                loggingId = "-".join([str(i+1),*list(experimentOptions.values()),startTime])
            else:
                loggingId = cloggingId
            experiment = Experiment(experimentOptions, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId)
            timeBeforeTransfer = time.time()
            experiment.runExperiment()
            timeAfterTransfer = time.time()
            TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
            logger.logPerformanceBenchmark(loggingId,f"TotaltransferTime : {TotaltransferTime}")
finally:
    logger.terminate_kafka_logger()