import time,os,configparser
from classes.experiments.OneStreamExperiment import OneStreamExperiment
from classes.experiments.MultipleStreamsExperiment import MultipleStreamsExperiment
from classes.KafkaLogger import KafkaLogger


# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

logger = KafkaLogger()

timeBeforeExperiment = time.time()

config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('configs/config1.ini')


# Define the path of the folder containing data files 
local_DataFolder_path = config.get('localServer', 'dataFolder_path')

# Define the remote file path
remote_DataFolder_path = config.get('remoteServer', 'dataFolder_path')


localPassword  = config.get('localServer', 'password')

remoteHostname = config.get('remoteServer', 'host')
remoteUsername = config.get('remoteServer', 'username')
remotePassword = config.get('remoteServer', 'password')





#Total tranfer time must always be calculated here

numberOfExperiments = config.getint('experiment', 'numberOfExperiments')
files = config.get('experiment', 'files').split(',')
#100 Mib and 200 Mib
#add function that converts Mib,kib,gib to bytes
limits = config.get('experiment', 'limits').split(',')
cloggingId = config.get('experiment', 'loggingId')

compressionTypes = config.get('experiment', 'compressionTypes').split(',')

streams = config.get('experiment', 'streams').split(',')

experiments = []
for stream in streams:
    stream = int(stream)
    for limit in limits:
        limit = int(limit)
        for file in files:
            local_file_path = local_DataFolder_path + file
            remote_file_path = f"{remote_DataFolder_path}{file}"
            for compressionType in compressionTypes:
                repetitions = []
                for i in range(0,numberOfExperiments):
                    if not cloggingId:
                        loggingId = "-".join([str(i+1),file,str(limit),str(stream),compressionType])
                    else:
                        loggingId = cloggingId
                    if stream == 1 : 
                        experiment = OneStreamExperiment(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId)
                    else:
                        experiment = MultipleStreamsExperiment(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword,stream,loggingId)


                    timeBeforeTransfer = time.time()
                    experiment.runExperiment()
                    timeAfterTransfer = time.time()
                    TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
                    logger.log(loggingId,f"TotaltransferTime : {TotaltransferTime}")

logger.terminate_kafka_logger()
