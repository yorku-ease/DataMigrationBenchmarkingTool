import subprocess
from datetime import datetime
import shutil
import os,time
import subprocess

from configparser import RawConfigParser
from KafkaLogger import KafkaLogger


logger = KafkaLogger()


# Specify the absolute path of the Bash script
bash_script_path = '/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/createDBs.sh'

# Run the Bash script and capture the output
result = subprocess.run([bash_script_path], capture_output=True, text=True)

# Print the output
print(result.stdout)

numberOfExperiments=2
streams = [1,3]
limits = ["104857600"]
compressionTypes = ["None"]

for stream in streams:
    for compressionType in compressionTypes:
        for limit in limits:
            timestamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")

            backup_name = timestamp + "backup.sql"
            for experimentNumber  in range(1,numberOfExperiments+1):
                # Generate the timestamp



                sourcedatadirPath="/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/sourcedatadir"
                backupsFolderPath="/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/"


                id = "-".join([str(experimentNumber),backup_name,limit,str(stream),compressionType])
                print(id)
                timeBeforeBackup = time.time()

                command = ['/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/runBackup.sh',backup_name,sourcedatadirPath,backupsFolderPath]
                timeAfterBackup = time.time()
                TotalBackupTime = timeAfterBackup - timeBeforeBackup

                logger.log(id,f"TotalBackupTime : {TotalBackupTime}")

                # Run the command and capture the output
                output = subprocess.check_output(command, universal_newlines=True)

                # Print the output
                print(output)

                shutil.copy('/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini', '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config2.ini')



                config = RawConfigParser()
                config.comment_prefixes = (';',)  # Set the prefix character for comments
                config.read('/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini')

                # Specify the source file path
                source_file = backupsFolderPath + backup_name

                # Specify the destination folder path
                destination_folder = config.get('localServer', 'dataFolder_path') 

                # Copy the file to the destination folder
                shutil.copy(source_file, destination_folder)

                config.set('experiment', 'files', backup_name)
                config.set('experiment', 'loggingId', id)
                config.set('experiment', 'limits', limit)
                config.set('experiment', 'compressiontypes', compressionType)
                config.set('experiment', 'streams', stream)


                # Writing our configuration file to 'example.ini'
                with open('/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini', 'w') as configfile:
                    config.write(configfile)

                limit = config.get('experiment', 'limits')

                # Specify the desired working directory
                working_directory = '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration'

                # Change the current working directory
                os.chdir(working_directory)
                #experiments_number=1
                output_path = "/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/output"
                timeBeforeMigration = time.time()
                subprocess.run(['/bin/python3.9', '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/Main.py'])
                timeAfterMigration = time.time()
                TotalMigrationTime = timeAfterMigration - timeBeforeMigration
                logger.log(id,f"TotalMigrationTime : {TotalMigrationTime}")


                os.remove("/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini")
                shutil.copy('/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config2.ini', '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config1.ini')
                os.remove("/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/configs/config2.ini")

                # Change the current working directory
                os.chdir("../")

                remote_folder = config.get('remoteServer', 'dataFolder_path') 
                remote_folder = remote_folder + backup_name  + "." + limit

                #command = ['/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/validatemigration.sh',source_file,remote_folder]

                # Run the command and capture the output
                #output = subprocess.check_output(command, universal_newlines=True)

                # Print the output
                #print(output)
                timeBeforeValidation = time.time()
                bash_script_path = '/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/validatemigration.sh'
                timeAfterValidation = time.time()
                TotalValidationTime = timeAfterValidation - timeBeforeValidation
                logger.log(id,f"TotalValidationTime : {TotalValidationTime}")
                # Specify the absolute path of the Bash script

                # Run the Bash script and capture the output

                #result = subprocess.run([bash_script_path,source_file,remote_folder], capture_output=True, text=True)

                #print("1")
                # Print the output
                #print(result.stdout)
                #print("2")
                
logger.terminatekafkalogger()