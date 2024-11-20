from myParser import Parser
import re
import json
import csv
import traceback
import configparser
from pymongo import MongoClient
import pandas as pd
class PerformanceBenchmarkParser(Parser):
    def __init__(self,log_file_path,json_file_path,csv_file_path,experiment_metadataHeader,streamMetrics,nonStreamMetrics):

        super().__init__(log_file_path,json_file_path,csv_file_path,experiment_metadataHeader)
        config = configparser.ConfigParser()
        config.comment_prefixes = (';',)  # Set the prefix character for comments
        config.read('config.ini')

        self.collection_name = config.get('mongo', 'performanceBenchmarkCollection_name')

        # Define a regular expression pattern to extract the key and key-value pairs
        self.log_pattern = r'Key=(.*?), Value=(.*?)$'
        self.experiment_metadataHeader = experiment_metadataHeader
        self.streamMetrics = streamMetrics
        self.nonStreamMetrics = nonStreamMetrics

    def toJsonData(self):
        # Compile the regular expression
        log_regex = re.compile(self.log_pattern)
        try:
            # Open the log file for reading
            with open(self.log_file_path, "r") as log_file:
                # Read and process each line in the log file
                for line in log_file:
                    # Find the key and key-value pairs in the log line
                    match = log_regex.search(line)

                    if match:
                        key = match.group(1)  # Extract the key
                        value_pairs = match.group(2).split(', ')  # Split key-value pairs into a list

                        # Create a dictionary to store the extracted key-value pairs
                        extracted_dict = {}

                        # Iterate through the value pairs and add them to the dictionary
                        for pair in value_pairs:
                            k, v = pair.split(' : ')
                            extracted_dict[k] = v
                        
                        index = key.index('-')
                        experimentNumber = key[:index]
                        key = key[index + 1:]

                        if key not in self.data :
                            self.data[key]= {}
                            self.data[key][experimentNumber] = {}
                            if "stream" in extracted_dict:
                                temp = next(iter(extracted_dict))
                                self.data[key][experimentNumber][int(extracted_dict["stream"])]={temp : extracted_dict[temp]}
                            else:
                                self.data[key][experimentNumber].update(extracted_dict)

                        else:
                            if experimentNumber not in self.data[key]:
                                self.data[key][experimentNumber] = {}
                            if "stream" in extracted_dict:
                                stream = extracted_dict["stream"]
                                if stream in self.data[key][experimentNumber]:
                                    temp = next(iter(extracted_dict))
                                    old_value = float(self.data[key][experimentNumber][stream].get(temp,0))
                                    new_value = str(float(extracted_dict[temp]) + old_value)
                                    self.data[key][experimentNumber][stream].update({temp : new_value})
                                else:
                                    temp = next(iter(extracted_dict))
                                    self.data[key][experimentNumber][stream] = {temp : extracted_dict[temp]}
                            else:
                                self.data[key][experimentNumber].update(extracted_dict)
                    else:
                        print("No match found in line:", line.strip())
        except FileNotFoundError:
            print(f"File '{self.log_file_path}' not found.")
        except IOError as e:
            print(f"Error reading the file: {e}")
        return self.data


    def writeCSVHeader(self):
        for key in self.nonStreamMetrics:
            self.experiment_metadataHeader.append(key)

        for key in self.streamMetrics:
            self.experiment_metadataHeader.append(key)         
        for key in self.streamMetrics:
            self.experiment_metadataHeader.append(f"sum{key}")        
            self.experiment_metadataHeader.append(f"max{key}")        
            self.experiment_metadataHeader.append(f"avg{key}")     
                
        with open(self.csv_file_path, 'w', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.experiment_metadataHeader)

    def toCSVfile(self):
        self.writeCSVHeader()

        for key in self.data.keys():
            row = key.split('-')
            p = list(row)
            for ikey in self.data[key].keys():
                try:
                    row = list(p)
                    row.insert(0,ikey)
                    for nSMetric in self.nonStreamMetrics:
                        row.append(self.data[key][ikey].get(nSMetric,0))
                    if "None" in self.data[key][ikey].keys():
                        for sMetric in self.streamMetrics:
                            row.append(self.data[key][ikey].get("None").get(sMetric))
                        row.extend(len(self.streamMetrics)*3*[0])
                    elif "1" in self.data[key][ikey].keys():
                        row.extend(len(self.streamMetrics)*[0])
                        streams = len([s for s in self.data[key][ikey].keys() if s.isdigit()])          
                        for sMetric in self.streamMetrics:
                            vsum = 0
                            maximum = -1
                            for i in range(1,streams + 1):

                                metricValue = float(self.data[key][ikey].get(str(i)).get(sMetric))
                                vsum +=  metricValue
                                maximum = max(maximum,metricValue)                       
                            avg = vsum / streams
                            row.append(vsum)
                            row.append(maximum)
                            row.append(avg)
                    else:
                        row.extend(len(self.streamMetrics)*4*[0])

                    with open(self.csv_file_path, 'a', encoding='UTF8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(row)   
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    traceback.print_exc()  