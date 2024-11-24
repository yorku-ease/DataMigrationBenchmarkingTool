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


dummyC = config.getboolean('migrationEnvironment', 'dummy')

print("dummy")
print(dummyC )
#Total tranfer time must always be calculated here

numberOfExperiments = config.getint('migrationEnvironment', 'numberOfExperiments')
cloggingId = config.get('migrationEnvironment', 'loggingId')
time_to_wait_beforeExperiment = config.getint('migrationEnvironment', 'time_to_wait_beforeExperiment')

if time_to_wait_beforeExperiment is None:
    time_to_wait_beforeExperiment = 0

experiments = config['experiment']
experimentsCombinations = Experiment.extractExperimentsCombinations(experiments)

def runExperiment(dummy = False):
    experimentStatus = False
    attempt_number = 0
    print("Controller : Value of Dummy is : " + str(dummy))
    while not experimentStatus and attempt_number < 3 :
        attempt_number += 1 
        if not cloggingId:
            if dummy : 
                dummyexperimentOptions = experimentOptions.copy()
                dummyexperimentOptions['tables'] = 'dummy'
                loggingId = "-".join([str(i+1),*list(dummyexperimentOptions.values()),str(attempt_number),startTime])
            else : 
                loggingId = "-".join([str(i+1),*list(experimentOptions.values()),str(attempt_number),startTime])
        else:
            loggingId = cloggingId   
        experiment = Experiment(experimentOptions, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId,dummy)
        timeBeforeTransfer = time.time()
        experimentStatus = experiment.runExperiment()
        timeAfterTransfer = time.time()
        TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
        logger.logPerformanceBenchmark(loggingId,f"TotalExperimentTime : {TotaltransferTime}")
        logger.logPerformanceBenchmark(loggingId,f"ExperimentStatus : {experimentStatus}")
        print(f"Sleeping for {time_to_wait_beforeExperiment} seconds.")
        time.sleep(time_to_wait_beforeExperiment)
        # Check if the experiment failed
        if not experimentStatus:
            print(f"Experiment {i+1} failed. Retrying after 600 seconds...")
            time.sleep(600)  
        else:
            print(f"Experiment {i+1} succeeded.")
    return experimentStatus
try:
    for experimentOptions in experimentsCombinations:
        startTime = str(time.time())
        for i in range(0,numberOfExperiments):
            if i == 0 and dummyC: 
                print("running the dummy experiment")
                dummy  = True
                experimentStatus = runExperiment(dummy)
                if not experimentStatus : 
                    break ; 
            print("running the real experiment ")
            print(experimentOptions)            
            experimentStatus = runExperiment(False)
            if not experimentStatus : 
                break    
        if not experimentStatus : 
            break ;        
finally:
    logger.terminate_kafka_logger()