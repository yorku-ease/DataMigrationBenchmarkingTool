import os,time
from classes.OneStreamExperiment import OneStreamExperiment
from classes.MultipleStreamsExperiment import MultipleStreamsExperiment
from classes.OutputNanager import OutputManager


# Define the path of the folder containing data files 
local_DataFolder_path = "data/"

# Define the remote file path
remote_DataFolder_path = "/home/" + os.environ.get('REMOTE1USERNAME') + "/data/"

localPassword  = os.environ.get('USERPASSWORD')

remoteHostname = os.environ.get('REMOTE1HOSTNAME')
remoteUsername = os.environ.get('REMOTE1USERNAME')
remotePassword = os.environ.get('REMOTE1PASSWORD')

file = "DS_001.csv"
local_file_path = local_DataFolder_path + file
remote_file_path = f"{remote_DataFolder_path}{file}"

compressionType = None
limit = 1000000000



experiment = OneStreamExperiment(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword)

#experiment = MultipleStreamsExperiment(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword,2)

#Total tranfer time must always be calculated here

experiments = []
numberOfExperiments = 3



for i in range(0,numberOfExperiments):
    timeBeforeTransfer = time.time()
    data = experiment.runExperiment()
    timeAfterTransfer = time.time()
    TotaltransferTime = timeAfterTransfer - timeBeforeTransfer

    data["TotaltransferTime"] = TotaltransferTime
    experiment.setOutput(data)
    experiments.append(experiment)

outputManager = OutputManager("output/test5.csv")

outputManager.writeCSVHeader(1)
outputManager.writeCSVContent(experiments)

# change the packet size and window size of sftp 