import time,os,configparser
from src.experiment import Experiment
from src.kafkaLogger import KafkaLogger

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
time_to_wait_beforeExperiment = config.getint('migrationEnvironment', 'time_to_wait_beforeExperiment')

if time_to_wait_beforeExperiment is None:
    time_to_wait_beforeExperiment = 0

experiments = config['experiment']
experimentsCombinations = Experiment.extractExperimentsCombinations(experiments)


try:
    for experimentOptions in experimentsCombinations:
        startTime = str(time.time())
        for i in range(0,numberOfExperiments):
            if not cloggingId:
                loggingId = "-".join([str(i+1),*list(experimentOptions.values()),startTime])
            else:
                loggingId = cloggingId   
            experimentStatus = False 
            retries = -1
            while not experimentStatus and retries < 5 :
                retries += 1 
                print(f"Sleeping for {time_to_wait_beforeExperiment} seconds.")
                time.sleep(time_to_wait_beforeExperiment)
                experiment = Experiment(experimentOptions, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId)
                timeBeforeTransfer = time.time()
                experimentStatus = experiment.runExperiment()
                timeAfterTransfer = time.time()
                TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
                logger.logPerformanceBenchmark(loggingId,f"TotalExperimentTime : {TotaltransferTime}")
                # Check if the experiment failed
                if not experimentStatus:
                    print(f"Experiment {i+1} failed. Retrying after 600 seconds...")
                    time.sleep(600)  # Wait 600 seconds before retrying
                else:
                    print(f"Experiment {i+1} succeeded.")
            if retries == 5 : 
                break    
        if retries == 5 : 
            break          
finally:
    logger.terminate_kafka_logger()