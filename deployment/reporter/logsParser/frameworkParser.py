from parser import Parser
import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd
class FrameworkParser(Parser):
    def __init__(self,log_file_path,json_file_path,csv_file_name):

        super().__init__(log_file_path,json_file_path,csv_file_name)
        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  # Set the prefix character for comments
        config.read('config.ini')

        self.collection_name = config.get('mongo', 'frameworklogsCollection_name')
        # Define a regular expression pattern to extract the key and key-value pairs
        self.log_pattern = r'Key=(.*?), Value=(.*?)$'
        self.header = ['Experiment Number','file','limit','compressionType','stream','Experiment startTime','logType','operation','statusOfOperation','timestamp']

