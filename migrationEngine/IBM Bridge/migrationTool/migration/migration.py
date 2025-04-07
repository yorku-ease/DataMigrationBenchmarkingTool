from db.db2database import Db2Database
from logger.kafkaLogger import KafkaLogger
import time,subprocess,random,re,os
from migration.http_client import HttpClient
from datetime import datetime
import json

class Migration:

    def __init__(self,conf):
        self.conf = conf
        self.logger = KafkaLogger()
        self.client = HttpClient(
        base_url="https://localhost:14080",
        username="admin",
        password="EWeBBqOF8LwcHDQI"
    )
    def str_to_bool(self,value):
        return str(value).strip().lower() in ("true", "1", "yes", "y")
    def clearDatabases(self):
        timeBeforeClear = time.time()
        targetdb2 = Db2Database(
            self.conf['targetDB2host'],
            self.conf['targetDB2Username'],
            self.conf['targetDB2Password'],
            self.conf['targetDB2Port'],
            self.conf['targetDB2type'],
            self.conf['sourceDatabasetoTargetDatabase'][1],
            self.conf['targetDB2Username'])
        
        targetdb2.clearDB(self.conf['tables'])

        #targetdb2Manager.clearCache(targetSshHost,targetSshPort,targetSshUsername,targetSshPassword,targetClearingscriptpath,targetContainerName)

        #sourcedb2Manager = Db2Database(sourceDB2host,sourceDB2Username,sourceDB2Password,sourceDB2Port,None,sourceDatabasetoTargetDatabase[0],sourceDB2Username)
        #DON'T RUN sourcedb2Manager.clearDB() otherwhise you'll lose data on source
        #sourcedb2Manager.clearCache(sourceSshHost,sourceSshPort,sourceSshUsername,sourceSshPassword,sourceClearingscriptpath,sourceContainerName)

        timeAfterClear = time.time()
        TotalClearTime = timeAfterClear - timeBeforeClear

        self.logger.logPerformanceBenchmark(self.conf['loggingId'],f"TotalClearTime : {TotalClearTime}")
    def createDefinition(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_name = f"job_{timestamp}"

        definition_payload = {
            "migration_job_name": job_name,
            "source_host": self.conf['sourceDB2host'],
            "target_host": self.conf['targetDB2host'],
            "source_user": self.conf['sourceDB2Username'],
            "target_user": self.conf['targetDB2Username'],
            "source_password": self.conf['sourceDB2Password'],
            "target_password": self.conf['targetDB2Password'],
            "source_database": self.conf['sourceDatabasetoTargetDatabase'][0],
            "target_database": self.conf['sourceDatabasetoTargetDatabase'][1],
            "source_port": self.conf['sourceDB2Port'],
            "target_port": self.conf['targetDB2Port'],
            "parallel_data_streams": self.conf['maxStreams'],
            "compression": self.conf['compress'],
            "binary": self.conf.get('binary'),
            "tables": self.conf['tables'],
            "whole_db": self.conf.get('whole_db', 'false'),
            "source_ssl": self.conf.get('source_ssl'),
            "target_ssl": self.conf.get('target_ssl'),
            "grants": self.conf.get('grants'),
            "hpu_mode": self.conf.get('hpu_mode'),
            "hpu_path": self.conf.get('hpu_path'),
            "backup_path": self.conf.get('backup_path'),
            "hidden_columns": self.conf.get('hidden_columns'),
            "maintenance_mode": self.conf.get('maintenance_mode'),

            "audit_policies": self.conf.get('audit_policies'),
            "roles": self.conf.get('roles'),
            "security_labels": self.conf.get('security_labels'),
            "security_label_components": self.conf.get('security_label_components'),
            "security_policies": self.conf.get('security_policies'),
            "histogram_templates": self.conf.get('histogram_templates'),
            "service_classes": self.conf.get('service_classes'),
            "bufferpools": self.conf.get('bufferpools'),
            "tablespaces": self.conf.get('tablespaces'),
            "comments": self.conf.get('comments'),
            "indexes": self.conf.get('indexes'),
            "sequences": self.conf.get('sequences'),
            "triggers": self.conf.get('triggers'),
            "views": self.conf.get('views'),
            "aliases": self.conf.get('aliases'),
            "procedures": self.conf.get('procedures'),
            "functions": self.conf.get('functions'),
            "constraints": self.conf.get('constraints'),
            "global_variables": self.conf.get('global_variables'),
            "modules": self.conf.get('modules'),
            "types": self.conf.get('types')
        }
        
        if self.conf['dummy'] : 
            definition_payload.update({
                "compression": random.choice(["GZIP", "LZ4", "NO"]),
                "parallel_data_streams": 10,
                "binary": False,
                "tables": [self.conf['sourceDB2Username'].upper() + '.' +self.conf["dummyTable"]]
            })
        # Create definition
        definition_url = "/migration/definitions/"
        definition_response = self.client.post(definition_url, definition_payload)

        if ( definition_response.get("status")):
            print(definition_response.get("status"))
        else: 
            print(definition_response)
        

        self.definition_id = definition_response.get("definition_id")
        print("definition_id: " + self.definition_id)

    def invokeMigration(self):
        # Ensure definition_id is available
        if self.definition_id:
            # Build the URL for the migration request
            invoke_url = f"/migration/migration_service_data_transfer/run/{self.definition_id}"

            invoke_response = self.client.post(invoke_url, {})

            if invoke_response.get("status")  :         
                print(invoke_response.get("status"))
            else: 
                print(invoke_response)

            self.job_id = invoke_response.get("job_id")
            print("job_id: " + self.job_id)
        else:
            # If no definition_id is available, print an error message
            print("No definition_id returned. Cannot trigger migration.")

    def getLogs(self):
        # Ensure job_id is available
        if self.job_id:
            # Build the URL for fetching logs
            logs_url = f"/migration/migration_service_data_transfer/jobs/{self.job_id}/logs"
            
            # Send the GET request to fetch logs
            logs_response = self.client.get(logs_url)

            # Print the status code of the logs request
            #print("Fetching Logs Response:", logs_response)
            
            logs = logs_response.get('log_content')

            return logs 
        
    def printLogs(self):
        log_file_path = "/app/exp.log"
        self.experimentstatus = "In progress"
        previous_log_lines = []
        precheckPattern  = r'Precheck.*?took (\d+):(\d+):(\d+\.\d+)'
        totalTimePattern = r'Total time: (\d+\.\d+)'
        
        totalPrecheck_time = 0
        total_time_value = 0

        while self.experimentstatus == "In progress":
            job_response = self.getJob()
            self.experimentstatus = job_response["jobs"].get("status")

            logs = self.getLogs()

            if logs:
                # Normalize logs into a list of lines
                if isinstance(logs, str):
                    current_log_lines = logs.splitlines()
                elif isinstance(logs, list):
                    current_log_lines = logs
                else:
                    print("Unrecognized log format")
                    break

                # Find new lines since the last check
                new_log_lines = current_log_lines[len(previous_log_lines):]

                if new_log_lines:
                    with open(log_file_path, 'a') as log_file:
                        for line in new_log_lines:
                            match = re.search(precheckPattern, line)
                            if match:
                                # Extract hours, minutes, and seconds from the match
                                hours, minutes, seconds = map(float, match.groups())
                                
                                # Convert hours, minutes, and seconds to seconds and add them to the total precheck time
                                totalPrecheck_time += hours * 3600 + minutes * 60 + seconds
                            
                            match = re.search(totalTimePattern, line)
                            if match:
                                total_time_value = float(match.group(1))
                            
                            self.logger.logMigrationEngine(self.conf['loggingId'], line.strip())
                            print(line.strip())  
                            log_file.write(line + '\n')

                # Update the previous logs
                previous_log_lines = current_log_lines
            else:
                print("No logs returned.")

            time.sleep(30)
        return total_time_value, totalPrecheck_time, self.experimentstatus

    def getJob(self):
        # Define the endpoint for fetching all migration jobs
        job_url = f"/migration/migration_service_data_transfer/jobs/{self.job_id}"
        
        # Send the GET request to fetch jobs
        job_response = self.client.get(job_url)

        return job_response



    def preExperiment(self):
        print("running pre experiment steps")

        if self.conf['dummy'] : 
            self.conf['tables'] = self.conf['dummyTable']

        self.clearDatabases()

    def runExperiment(self):
        print("running experiment")
        self.createDefinition()
        self.invokeMigration()
        self.total_time_value, self.totalPrecheck_time, self.experimentstatus = self.printLogs()
        #cmd = self.buildCommand()

    def postExperiment(self):
        print("running post experiment steps")
        print("total time: ", self.total_time_value)
        print("total precheck time: ", self.totalPrecheck_time)

        if self.experimentstatus == "Error":
            print("[EXP001] Experiment Status: Failed")
        elif self.experimentstatus == "Success" :
            print("[EXP001] Experiment Status: Succeeded")

        self.logger.logPerformanceBenchmark(self.conf['loggingId'],f"TotaltransferTime : {self.total_time_value}")
        self.logger.logPerformanceBenchmark(self.conf['loggingId'],f"totalPrecheckTime : {self.totalPrecheck_time}")
        pass