from performanceBenchmarkParser import PerformanceBenchmarkParser
import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd
class Db2PerformanceBenchmarkParser(PerformanceBenchmarkParser):
    def __init__(self,log_file_path,json_file_path,csv_file_path):

        super().__init__(log_file_path,json_file_path,csv_file_path)

        self.header = ['Experiment Number','compress','maxStreams','sourceDatabasetoTargetDatabase','tables','Experiment startTime']
        self.streamMetrics = []
        self.nonStreamMetrics = ['TotalExperimentTime','TotaltransferTime','totalPrecheckTime']
