import time
from classes.OneStreamExperiment import OneStreamExperiment
from classes.MultipleStreamsExperiment import MultipleStreamsExperiment
from classes.KafkaLogger import KafkaLogger


import configparser

logger = KafkaLogger()

timeBeforeExperiment = time.time()

config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini')


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
                    data = experiment.runExperiment()
                    timeAfterTransfer = time.time()
                    TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
                    logger.log(loggingId,f"TotaltransferTime : {TotaltransferTime}")
#                    data["TotaltransferTime"] = TotaltransferTime
#                    experiment.setOutput(data)
#                    repetitions.append(experiment)
#                experiments.append(repetitions)




#outputManager = OutputManager(config.get('output', 'path'))

#outputManager.writeCSVHeader()
#for experiment in experiments:
#    outputManager.writeCSVContent(experiment)

#timeAfterExperiment = time.time()
#totalExperimentTime = (timeAfterExperiment - timeBeforeExperiment)/3600
#outputManager.writeTotalExperimentTime(totalExperimentTime)

logger.terminate_kafka_logger()
