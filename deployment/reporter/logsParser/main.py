from frameworkParser import FrameworkParser
from performanceBenchmarkParser import PerformanceBenchmarkParser
from db2PerformanceBenchmarkParser import Db2PerformanceBenchmarkParser
from migrationEngineParser import MigrationEngineParser
from db2migrationEngineParser import Db2MigrationEngineParser
import configparser
import os
# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)
config = configparser.ConfigParser()
config.comment_prefixes = (';',)  # Set the prefix character for comments
config.read('config.ini')
migrationEngineName = config.get('migrationEngine', 'name')


parsers = []
parsers.append(FrameworkParser("../kafkacluster/framework.log","framework.json","framework.csv"))

# Define the path of the folder containing data files 

if migrationEngineName.lower() == "db2":
    print("We'll use DB2 logs Parser as specified in config.ini ! ")
    parsers.append(Db2PerformanceBenchmarkParser("../kafkacluster/performanceBenchmark.log","performanceBenchmark.json","performanceBenchmark.csv"))
    parsers.append(Db2MigrationEngineParser("../kafkacluster/migrationEngine.log","migrationEngine.json","migrationEngine.csv"))
elif migrationEngineName.lower() =="default":
    print("We'll use Default Engine logs Parser as specified in config.ini ! ")
    parsers.append(PerformanceBenchmarkParser("../kafkacluster/performanceBenchmark.log","performanceBenchmark.json","performanceBenchmark.csv"))
    parsers.append(MigrationEngineParser("../kafkacluster/migrationEngine.log","migrationEngine.json","migrationEngine.csv"))
elif migrationEngineName.lower() == "fivetran":
    print("We'll use Fivetran logs Parser as specified in config.ini ! ")
    parsers.append(PerformanceBenchmarkParser("../kafkacluster/performanceBenchmark.log","performanceBenchmark.json","performanceBenchmark.csv"))
    parsers.append(MigrationEngineParser("../kafkacluster/migrationEngine.log","migrationEngine.json","migrationEngine.csv"))

print("start Parsing ! ")
for parser in parsers:
    parser.toJsonData()
    parser.toJsonfile()
    parser.toCSVfile()
    parser.SavetoDB()

print("Parsing done !")