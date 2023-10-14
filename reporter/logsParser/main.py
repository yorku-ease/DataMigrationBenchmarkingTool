from parser import Parser
import os
# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

p = Parser("../kafka cluster/output.log")
data = p.parsetoJson()
p.saveJson("data.json")
p.parsetoCSV("data.csv")
