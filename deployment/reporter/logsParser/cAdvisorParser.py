import json
import configparser
from pymongo import MongoClient

class CAdvisorParser():


    def __init__(self,log_file_path):
        self.log_file_path = log_file_path
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
        

                    
    def SavetoDB(self):

        # Connect to MongoDB
        client = MongoClient(
        host = [ str(self.mongo_host) + ":" + str(self.mongo_port) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = self.mongo_user,
        password = self.mongo_password)
        db = client[self.database_name]
        collection = db["cAdvisorData"]

        batch_size = 100
        with open(self.log_file_path, 'r') as file:
            batch = []
            i = 0
            for line in file:
                i += 1
                print(i)
                line = line.strip()
                if line: 
                    data = json.loads(line)
                batch.append(data)
                if len(batch) == batch_size:
                    # Insert batch into MongoDB
                    collection.insert_many(batch)
                    batch.clear()
            if batch:
                # Insert remaining lines if they exist
                collection.insert_many(batch)



        # Close MongoDB connection
        client.close()    