from myParser import Parser
import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd
class MigrationEngineParser(Parser):
    def __init__(self,log_file_path,json_file_path,csv_file_name,experiment_metadataHeader,log_detailsHeader):

        super().__init__(log_file_path,json_file_path,csv_file_name,experiment_metadataHeader)
        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  # Set the prefix character for comments
        config.read('config.ini')

        self.collection_name = config.get('mongo', 'migrationEnginelogsCollection_name')
        # Define a regular expression pattern to extract the key and key-value pairs
        self.log_pattern = r'Key=(.*?), Value=(.*?)$'
        self.experiment_metadataHeader = experiment_metadataHeader
        self.log_detailsHeader = log_detailsHeader 
        self.header = self.experiment_metadataHeader + self.log_detailsHeader

 