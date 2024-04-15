from frameworkParser import FrameworkParser
from performanceBenchmarkParser import PerformanceBenchmarkParser
from db2PerformanceBenchmarkParser import Db2PerformanceBenchmarkParser
from migrationEngineParser import MigrationEngineParser
import os
# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)
parsers = []
parsers.append(Db2PerformanceBenchmarkParser("../kafkacluster/performanceBenchmark.log","performanceBenchmark.json","performanceBenchmark.csv"))
parsers.append(FrameworkParser("../kafkacluster/framework.log","framework.json","framework.csv"))
parsers.append(MigrationEngineParser("../kafkacluster/migrationEngine.log","migrationEngine.json","migrationEngine.csv"))

for parser in parsers:
    parser.toJsonData()
    parser.toJsonfile()
    parser.toCSVfile()
    parser.SavetoDB()