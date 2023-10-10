from classes.migrationEngine.defaultEngine.DefaultFileMigrator import DefaultFileMigrator
import subprocess
from threading import Thread
from classes.KafkaLogger import KafkaLogger



class Experiment(Thread):

    output : dict

    def __init__(self, local_file_path, remote_file_path, compressionType, limit,streams, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.compressionType = compressionType
        self.limit = limit
        self.remoteHostname = remoteHostname
        self.remoteUsername = remoteUsername
        self.remotePassword = remotePassword
        self.localPassword = localPassword
        self.streams = streams
        self.loggingId = loggingId
        self.logger = KafkaLogger()




    def clearRamCacheSwap(self,ssh,sftp):

        # Specify the desired working directory
        #working_directory = '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration'

        # Change the current working directory
        #os.chdir(working_directory)
        # Copy the file to the remote machine
        #sftp.put("clearcache.sh", "clearcache.sh")

        
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

    def setOutput(self, data):

        self.output = data

    def getOutput(self):

        return self.output
   
    def getFilename(self):

        return self.local_file_path.split('/')[-1]
   
    def getCompressionType(self):
        
        return self.compressionType
   
    def getLimit(self):

        return self.limit
    def getStreamsNumber(self):

        return self.streams
                        
    def runExperiment(self):
        
        migrationEngine = DefaultFileMigrator(self.remoteHostname,self.remoteUsername,self.remotePassword,self.localPassword,self.loggingId,self.logger)
        migrationEngine.migrate(self.local_file_path,self.remote_file_path,self.compressionType,self.limit,self.streams)
    
