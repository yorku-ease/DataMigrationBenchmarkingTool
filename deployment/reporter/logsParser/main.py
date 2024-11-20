from frameworkParser import FrameworkParser
from performanceBenchmarkParser import PerformanceBenchmarkParser
#from db2PerformanceBenchmarkParser import Db2PerformanceBenchmarkParser
from migrationEngineParser import MigrationEngineParser
from db2migrationEngineParser import Db2MigrationEngineParser
from cAdvisorParser import CAdvisorParser


import configparser
import os
# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)
config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('config.ini')
migrationEngineName = config.get('migrationEngine', 'name').lower()

headers_map = {
    "db2": {
        "experiment_metadataHeader": ['Experiment Number','compress','sourceDatabasetoTargetDatabase','tables','maxStreams','binary','attempt_number','Experiment startTime'] ,
        "streamMetrics": [],
        "nonStreamMetrics": ['TotalExperimentTime','TotaltransferTime','totalPrecheckTime','TotalClearTime','ExperimentStatus'],
        "log_detailsHeader": ['logTime','logType','logLocation','logDescription'],
    },
    "default": {
        "experiment_metadataHeader":  ['Experiment Number','file','limit','compressionType','stream','Experiment startTime'],
        "streamMetrics": ['sizeOnTargetMachine','sizeOnLocalMachine','compressionTime','dataTransferTime','readingFileTime'] ,
        "nonStreamMetrics": ['TotalBackupTime','TotaltransferTime','TotalMigrationTime','TotalValidationTime','TotalClearTime'],
        "log_detailsHeader": ['logType','operation','statusOfOperation','timestamp'],
    },
    "fivetran": {
        "experiment_metadataHeader": ['Experiment Number','sourceDatabasetoTargetDatabase','tables','attempt_number','Experiment startTime'],
        "streamMetrics": [],
        "nonStreamMetrics":['TotalExperimentTime','TotaltransferTime','TotalClearTime','ExperimentStatus'],
        "log_detailsHeader": ['logType','operation','statusOfOperation','timestamp'],
    }
}



experiment_metadataHeader = headers_map.get(migrationEngineName).get("experiment_metadataHeader")
streamMetrics = headers_map.get(migrationEngineName).get("streamMetrics")
nonStreamMetrics = headers_map.get(migrationEngineName).get("nonStreamMetrics")
log_detailsHeader = headers_map.get(migrationEngineName).get("log_detailsHeader")

engineParsers = {
    "db2": 
        Db2MigrationEngineParser("../kafkacluster/migrationEngine.log", "migrationEngine.json", "migrationEngine.csv",experiment_metadataHeader,log_detailsHeader)
    ,
    "default": 
        MigrationEngineParser("../kafkacluster/migrationEngine.log", "migrationEngine.json", "migrationEngine.csv",experiment_metadataHeader,log_detailsHeader)
    ,
    "fivetran": 
        MigrationEngineParser("../kafkacluster/migrationEngine.log", "migrationEngine.json", "migrationEngine.csv",experiment_metadataHeader,log_detailsHeader)
    
}


parsers = []
parsers.append(engineParsers.get(migrationEngineName))
parsers.append(FrameworkParser("../kafkacluster/framework.log","framework.json","framework.csv",experiment_metadataHeader,log_detailsHeader))
parsers.append(PerformanceBenchmarkParser("../kafkacluster/performanceBenchmark.log","performanceBenchmark.json","performanceBenchmark.csv",experiment_metadataHeader,streamMetrics,nonStreamMetrics))

print("start Parsing ! ")
for parser in parsers:
    parser.toJsonData()
    parser.toJsonfile()
    parser.toCSVfile()
    parser.SavetoDB()

cAdvisorParser = CAdvisorParser("../kafkacluster/cadvisor.log")
cAdvisorParser.SavetoDB()

print("Parsing done !")