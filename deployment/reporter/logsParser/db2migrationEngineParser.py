from myParser import Parser
import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd
class Db2MigrationEngineParser(Parser):
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
          
    def toJsonData(self):
               # Compile the regular expression
        self.data = []
        
        extracted_dict = {}
        log_regex = re.compile(self.log_pattern)
        try:
            # Open the log file for reading
            with open(self.log_file_path, "r") as log_file:
                # Read and process each line in the log file
                for line in log_file:
                    # Find the key and key-value pairs in the log line
                    match = log_regex.search(line)

                    if match:
                        key = match.group(1).split('-')  # Extract the key
                        value =  match.group(2)
                        value_pairs = match.group(2).split(' | ')  # Split key-value pairs into a list

                        # Create a dictionary to store the extracted key-value pairs
                        extracted_dict = {}
                        for i in range(0,8):
                            extracted_dict[self.header[i]] = key[i]
                        if (len(value_pairs)>1):
                            for i in range(8,len(self.header)):
                                if 0 <= i - 8 < len(value_pairs)  : 
                                    extracted_dict[self.header[i]] = value_pairs[i - 8].strip()
                                else: 
                                    extracted_dict[self.header[i]] = ""
                        else : 
                            extracted_dict['description'] = value

                    self.data.append(extracted_dict)
            
            return extracted_dict
        except FileNotFoundError:
            print(f"File '{self.log_file_path}' not found.")
        except IOError as e:
            print(f"Error reading the file: {e}") 

    def toCSVfile(self):
        try:
            with open(self.csv_file_path, 'w', encoding='UTF8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.header)
                for row in self.data:
                    values = list(row.values())

                    if (len(values)<len(self.header)):
                        commas = ([''] * (len(self.header) - len(values))) 
                        values = values[:-1] + commas  + [values[-1]]
                        
                                         

                    writer.writerow(values)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            traceback.print_exc()     