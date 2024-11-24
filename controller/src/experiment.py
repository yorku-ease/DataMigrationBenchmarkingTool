import time,sys,traceback,os,shutil,configparser,docker,paramiko,subprocess,yaml,threading
from threading import Thread
from src.kafkaLogger import KafkaLogger
from src.connectionManager import ConnectionManager
from src.dockerComposeParser import DockerComposeParser
from itertools import product



class Experiment(Thread):

    output : dict
    experimentStatus : bool

    def __init__(self, experimentOptions, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId,dummy = False):
        self.experimentOptions = experimentOptions
 
        self.remoteHostname = remoteHostname
        self.remoteUsername = remoteUsername
        self.remotePassword = remotePassword
        self.localPassword = localPassword
        self.loggingId = loggingId
        self.logger = KafkaLogger()
        self.dummy = dummy

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
            return self.experimentStatus
        except Exception as e:
            timestamp = time.time()
            error_message = str(e)
            error_location = f"File: {__file__}, Function: {__name__}, Line: {sys.exc_info()[-1].tb_lineno}"
            exception_type = type(e).__name__
            message = f"type : error, Timestamp : {timestamp}, ErrorMessage : {error_message} {error_location} ExceptionType: {exception_type}"
            self.logger.logFramework(self.loggingId,message)
            stack_trace = traceback.format_exc()
            print(message)
            print(stack_trace)
            
    def containerLog(self,container,service_name):
        log_generator = container.logs(stream=True)
        log_code = "[EXP001] "  
        log_text = log_code + "Experiment Status: " 
        for log in log_generator:
            print("log " + service_name + " : " +log.decode('utf-8'), end="")  # Print each log line
            if  log_text + "Succeeded" in log.decode('utf-8'):
                self.experimentStatus = True
            elif log_text + "Failed" in log.decode('utf-8'):
                self.experimentStatus = False

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
        if self.dummy : 
            config.set('migrationEnvironment', 'dummy', True)
        else : 
            config.set('migrationEnvironment', 'dummy', False)
        # Writing our configuration file to 'example.ini'
        with open(f'configs/migrationEngineConfig.ini', 'w') as configfile:
            config.write(configfile)

    def removeConfigFile(self):
        os.remove("configs/migrationEngineConfig.ini")
        shutil.copy('configs/migrationEngineConfig1.ini', 'configs/migrationEngineConfig.ini')
        os.remove("configs/migrationEngineConfig1.ini")


    def migrate(self):
        
        try:
            containers = []
            loggingThreads = []
            self.experimentStatus = False
            FOLDERS_PATH = os.environ.get("FOLDERS_PATH")
            
            config = configparser.RawConfigParser()
            config.comment_prefixes = (';',)  
            
            # Set the prefix character for comments
            config.read(f'configs/config.ini')

            self.createMigrationEngineConfig()

            client = docker.from_env()

            composeParser = DockerComposeParser("configs/docker-compose.yml")

            compose_data = composeParser.parseFile()
            volumes = {
              #  f"{FOLDERS_PATH}/data": {"bind": "/app/data", "mode": "rw"},
                f"{FOLDERS_PATH}/configs": {"bind": "/app/configs", "mode": "rw"},
            }
            labels = {
            'loggingId': self.loggingId,
            }
            for network_name, network_config in compose_data.get('networks', {}).items():
                client.networks.create(network_name, **network_config)
            for volume_name, volume_config in compose_data.get('volumes', {}).items():
                client.volumes.create(name=volume_name, **volume_config)
            print(compose_data.get('services', {}).items())
            for service_name, service_config in compose_data.get('services', {}).items():
                print(service_config.get('ports'))
                container_name =  "MigrationEngine_"+ service_name  + "-" + self.loggingId
                additional_volume = f"{FOLDERS_PATH}/configs:/app/configs:rw"

                if service_config.get('volumes') is None:
                    service_config['volumes'] = [additional_volume]
                elif isinstance(service_config['volumes'], list):
                    service_config['volumes'].append(additional_volume)

                try:
                    oldContainer = client.containers.get(container_name)
                    oldContainer.stop()
                    oldContainer.remove()
                except docker.errors.NotFound:
                    pass
                resources = composeParser.parseResources(service_config.get('deploy', {}).get('resources', {}))
                try : 
                    container = client.containers.run(
                    image=service_config['image'],
                    name=container_name,
                    environment=service_config.get('environment'),
                    ports=composeParser.parsePorts(service_config.get('ports')),
                    volumes=service_config.get('volumes'),
                    network=service_config.get('network'),
                    labels = labels,
                    command=service_config.get('command'),
                    privileged=service_config.get('privileged'),
                    cpu_quota=resources['cpu_quota'],
                    cpu_period=resources['cpu_period'],
                    cpu_shares=resources['cpu_shares'],
                    mem_limit=resources['mem_limit'],
                    mem_reservation=resources['mem_reservation'],
                    detach=True  # Run in the background
                )
                except Exception as e:
                    timestamp = time.time()
                    error_message = str(e)
                    error_location = f"File: {__file__}, Function: {__name__}, Line: {sys.exc_info()[-1].tb_lineno}"
                    exception_type = type(e).__name__
                    message = f"type : error, Timestamp : {timestamp}, ErrorMessage : {error_message} {error_location} ExceptionType: {exception_type}"
                    self.logger.logFramework(self.loggingId,message)
                    stack_trace = traceback.format_exc()
                    print(message)
                    print(stack_trace)
                log_thread = threading.Thread(target=self.containerLog, args=(container,service_name))

                # Start the thread
                loggingThreads.append(log_thread.start())

                containers.append(container)

            for container in containers: 
                container.wait()



            
            self.removeConfigFile()
        except Exception as e:
            timestamp = time.time()
            error_message = str(e)
            error_location = f"File: {__file__}, Function: {__name__}, Line: {sys.exc_info()[-1].tb_lineno}"
            exception_type = type(e).__name__
            message = f"type : error, Timestamp : {timestamp}, ErrorMessage : {error_message} {error_location} ExceptionType: {exception_type}"
            self.logger.logFramework(self.loggingId,message)
            stack_trace = traceback.format_exc()
            print(message)
            print(stack_trace)
        finally:
            for container in containers:
                if container is not None:
                    print("stopping")
                    container.stop()
                    print("stopping")
                    container.remove()
            return self.experimentStatus