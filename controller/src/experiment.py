import time,sys,traceback,os,shutil,configparser,docker,paramiko,subprocess
from threading import Thread
from src.kafkaLogger import KafkaLogger
from src.connectionManager import ConnectionManager
from itertools import product



class Experiment(Thread):

    output : dict

    def __init__(self, experimentOptions, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId):
        self.experimentOptions = experimentOptions
 
        self.remoteHostname = remoteHostname
        self.remoteUsername = remoteUsername
        self.remotePassword = remotePassword
        self.localPassword = localPassword
        self.loggingId = loggingId
        self.logger = KafkaLogger()

    @staticmethod
    def extractExperimentsCombinations(experiments):
        experimentLists = dict(experiments)
        experimentLists = {key: value.split(',') if ',' in value else [value] for key, value in experimentLists.items()}

        # Generate all combinations
        experimentsCombinations = list(product(*experimentLists.values()))

        # Create a list of dictionaries with combinations
        experimentsCombinations = [dict(zip(experimentLists.keys(), combination)) for combination in experimentsCombinations]
        return experimentsCombinations

    def connect(self):
        connectionManager = ConnectionManager(self.remoteHostname, self.remoteUsername, self.remotePassword)
        try:
            connectionManager.connect()

        except paramiko.SSHException as sshException:
            print('Unable to establish SSH connection: %s' % sshException)
        except paramiko.SFTPError as sftpError:
            print('Unable to open SFTP session: %s' % sftpError)
        return connectionManager
    

    def clearRamCacheSwap(self):
        self.logger.logFramework(self.loggingId,f"type : info, clearRamCacheSwap : started, Timestamp : {time.time()}")
        connectionManager = self.connect()
        ssh = connectionManager.get_SSH()
        sftp = connectionManager.get_SFTP()

        
        # Change the current working directory
        #os.chdir(working_directory)
        # Copy the file to the remote machine
        sftp.put("clearcache.sh", "clearcache.sh")

        sftp.chmod("clearcache.sh", 0o755)

        #clear RAM Cache as well as Swap Space at local machine
        result = subprocess.run([f"echo {self.localPassword} | ./clearcache.sh"], stdout=subprocess.PIPE, shell=True)
        # Print the output of the command
        print(result.stdout.decode('utf-8'))

        #output = subprocess.check_output([f"echo {self.localPassword} | ./clearcache.sh"],shell=True)
        #print(output.decode("utf-8"))
        print("On local machine")
        #clear RAM Cache as well as Swap Space at remote machine

        stdin, stdout, stderr = ssh.exec_command(f"echo {self.remotePassword} | ./clearcache.sh")
        output = stdout.read().decode("utf-8")

        # Print output 
        print(output)
        print("On remote machine")
        connectionManager.close()
        self.logger.logFramework(self.loggingId,f"type : info, clearRamCacheSwap : completed, Timestamp : {time.time()}")

                        
    def runExperiment(self):

        try:
            timeBeforeClear = time.time()
            #self.clearRamCacheSwap()
            timeAfterClear = time.time()
            TotalClearTime = timeAfterClear - timeBeforeClear
            self.logger.logPerformanceBenchmark(self.loggingId,f"TotalClearTime : {TotalClearTime}")
            self.logger.logFramework(self.loggingId,f"type : info, Experiment : started, Timestamp : {time.time()}")
            # Log error information
            self.migrate()
            self.logger.logFramework(self.loggingId,f"type : info, Experiment : completed, Timestamp : {time.time()}")
        except Exception as e:
            timestamp = time.time()
            error_message = str(e)
            error_location = f"File: {__file__}, Function: {__name__}, Line: {sys.exc_info()[-1].tb_lineno}"
            exception_type = type(e).__name__
            message = f"type : error, Timestamp : {timestamp}, ErrorMessage: {error_message}, {error_location}, ExceptionType: {exception_type}"
            self.logger.logFramework(self.loggingId,message)
            stack_trace = traceback.format_exc()
            print(message)
            print(stack_trace)

    def createMigrationEngineConfig(self):
        FOLDERS_PATH = os.environ.get("FOLDERS_PATH")
        
        try:
            # Try to open the file in write mode
            with open('configs/migrationEngineConfig.ini', "w") as file:
                # Writing an empty string to create the file
                file.write("")
        except FileNotFoundError:
            print("Error: The specified path or file name is invalid.")
        except Exception as e:
            print(f"An error occurred: {e}")
        #prepare the configuration file for the migration engine 
        shutil.copy(f'configs/migrationEngineConfig.ini', f'configs/migrationEngineConfig1.ini')



        config = configparser.RawConfigParser()
        config.comment_prefixes = (';',)  
        
        # Set the prefix character for comments
        config.read(f'configs/config.ini')

        for key in self.experimentOptions:
            config.set('experiment', key, self.experimentOptions[key])

        config.set('migrationEnvironment', 'loggingId', self.loggingId)
        


        # Writing our configuration file to 'example.ini'
        with open(f'configs/migrationEngineConfig.ini', 'w') as configfile:
            config.write(configfile)

    def removeConfigFile(self):
        os.remove("configs/migrationEngineConfig.ini")
        shutil.copy('configs/migrationEngineConfig1.ini', 'configs/migrationEngineConfig.ini')
        os.remove("configs/migrationEngineConfig1.ini")


    def migrate(self):
        
        try:
            container = None

            FOLDERS_PATH = os.environ.get("FOLDERS_PATH")
            
            config = configparser.RawConfigParser()
            config.comment_prefixes = (';',)  
            
            # Set the prefix character for comments
            config.read(f'configs/config.ini')

            self.createMigrationEngineConfig()

            client = docker.from_env()
            image_name = config.get('migrationEnvironment', 'migrationEngineDockerImage')
            container_name = "MigrationEngine"

            volumes = {
                f"{FOLDERS_PATH}/data": {"bind": "/app/data", "mode": "rw"},
                f"{FOLDERS_PATH}/configs": {"bind": "/app/configs", "mode": "rw"},
            }
            labels = {
            'loggingId': self.loggingId,
            }
            try:
                container = client.containers.get(container_name)
                container.remove()
            except docker.errors.NotFound:
                pass
            container = None
            existing_containers = client.containers.list(all=True)
            container_exists = any(container.name == container_name for container in existing_containers)

            '''if container_exists:
                container = client.containers.get(container_name)
                container.restart()
            else:'''
            ports = {
    '50050': 50050,
    '13080': 13080,
    '14080': 14080
}
            #Run the migration engine in a docker container as a sibling to the container running this code.
            container = client.containers.run(
                privileged = True,
                #mem_limit = "0",
                volumes=volumes,
                image=image_name,
                name=container_name,
                labels=labels,
                detach= True,
                ports=ports  # Add the 'ports' parameter

                #cpuset_cpus = "0",
            )
            log_generator = container.logs(stream=True)
            for log in log_generator:
                print(log.decode('utf-8'), end="")  # Print each log line

            container.wait()


            self.removeConfigFile()

        finally:
            if container is not None:
                container.remove()