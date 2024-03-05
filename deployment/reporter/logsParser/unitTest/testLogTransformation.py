import sys
import os
import unittest,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)


from frameworkParser import FrameworkParser
from performanceBenchmarkParser import PerformanceBenchmarkParser
from migrationEngineParser import MigrationEngineParser


class TestLogTransformation(unittest.TestCase):

    def test_PerformanceBenchmarkParser(self):
        parser = PerformanceBenchmarkParser("unitTest/performanceBenchmark.log","unitTest/operformanceBenchmark.json","unitTest/operformanceBenchmark.csv")
        parser.toJsonData()
        parser.toJsonfile()
        output_data = json.dumps(parser.toJsonData(), sort_keys=True)
        with open("unitTest/operformanceBenchmark.json", 'r') as output_file:
            output_data = json.dumps(json.load(output_file), sort_keys=True)
        with open("unitTest/eperformanceBenchmark.json", 'r') as expected_file:
            expected_data = json.dumps(json.load(expected_file), sort_keys=True)
        self.assertEqual(expected_data, output_data)
      
    def test_FrameworkParser(self):
        parser = FrameworkParser("unitTest/framework.log","unitTest/oframework.json","unitTest/oframework.csv")
        parser.toJsonData()
        parser.toJsonfile()
        output_data = json.dumps(parser.toJsonData(), sort_keys=True)
        with open("unitTest/oframework.json", 'r') as output_file:
            output_data = json.dumps(json.load(output_file), sort_keys=True)        
        with open("unitTest/eframework.json", 'r') as expected_file:
            expected_data = json.dumps(json.load(expected_file), sort_keys=True)
        self.assertEqual(expected_data, output_data)

    def test_MigrationEngineParser(self):
        parser = MigrationEngineParser("unitTest/migrationEngine.log","unitTest/omigrationEngine.json","unitTest/omigrationEngine.csv")
        parser.toJsonData()
        parser.toJsonfile()
        output_data = json.dumps(parser.toJsonData(), sort_keys=True)
        with open("unitTest/omigrationEngine.json", 'r') as output_file:
            output_data = json.dumps(json.load(output_file), sort_keys=True)
        with open("unitTest/emigrationEngine.json", 'r') as expected_file:
            expected_data = json.dumps(json.load(expected_file), sort_keys=True)
        self.assertEqual(expected_data, output_data)

if __name__ == '__main__':
    unittest.main()