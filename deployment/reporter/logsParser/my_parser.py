import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd

class Parser():


    def __init__(self,log_file_path,json_file_path,csv_file_path):
        self.log_file_path = log_file_path
        self.json_file_path = json_file_path
        self.csv_file_path = csv_file_path
        self.data = {}

        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  # Set the prefix character for comments
        config.read('config.ini')


        # Define the path of the folder containing data files 
        self.mongo_host = config.get('mongo', 'host')
        self.mongo_port = int(config.get('mongo', 'port'))
        self.mongo_user = config.get('mongo', 'user')
        self.mongo_password = config.get('mongo', 'password')
        self.database_name = config.get('mongo', 'database_name')





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
                        value_pairs = match.group(2).split(', ')  # Split key-value pairs into a list

                        # Create a dictionary to store the extracted key-value pairs
                        extracted_dict = {}
                        for i in range(0,6):
                            extracted_dict[self.header[i]] = key[i]
                        # Iterate through the value pairs and add them to the dictionary
                        for pair in value_pairs:
                            k, v = pair.split(' : ')
                            extracted_dict[k] = v
                    self.data.append(extracted_dict)
            
            return extracted_dict
        except FileNotFoundError:
            print(f"File '{self.log_file_path}' not found.")
        except IOError as e:
            print(f"Error reading the file: {e}")
    def toJsonfile(self):
        with open(self.json_file_path, "w") as json_file:
            # Serialize and write the dictionary to the file as JSON data
            json.dump(self.data, json_file, indent=4)  # The 'indent' parameter is optional and adds formatting for readability

    def toCSVfile(self):
        try:
            with open(self.csv_file_path, 'w', encoding='UTF8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.header)
                for row in self.data:
                    i = 7
                    values = list(row.values())
                    operation = list(row.keys())[i]
                    values.insert(i, operation)
                    writer.writerow(values)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            traceback.print_exc()            

                    
    def SavetoDB(self):

        # Connect to MongoDB
        client = MongoClient(
        host = [ str(self.mongo_host) + ":" + str(self.mongo_port) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = self.mongo_user,
        password = self.mongo_password)
        db = client[self.database_name]
        collection = db[self.collection_name]


        df = pd.read_csv(self.csv_file_path)

        # Convert DataFrame to a list of dictionaries (each row becomes a dictionary)
        dBdata = df.to_dict(orient='records')

        if dBdata:
            collection.insert_many(dBdata)

        # Close MongoDB connection
        client.close()    