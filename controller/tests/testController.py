import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import configparser
from src.experiment import Experiment
from unittest.mock import patch

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

class TestExperiment(unittest.TestCase):

    @patch('src.experiment.KafkaLogger')
    def test_createMigrationEngineConfig(self,mock_KafkaLogger):
        mock_KafkaLogger.return_value=None
        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  
        config.read('configs/config.ini')
        experiments = config['experiment']
        experimentsCombinations = Experiment.extractExperimentsCombinations(experiments)
        for i in range(len(experimentsCombinations)):
             experiment = Experiment(experimentsCombinations[i], None, None, None, None, None)
             experiment.createMigrationEngineConfig()
             expectedMigrationEngineConfigfile = f"expectedConfigfiles/config{i+1}.ini"
             with open(expectedMigrationEngineConfigfile, 'r') as file1, open('configs/migrationEngineConfig.ini', 'r') as file2:
                content1 = file1.read()
                content2 = file2.read()
                self.assertEqual(content1, content2)
        experiment.removeConfigFile()    

if __name__ == '__main__':
    unittest.main()