from classes.ConnectionManager import ConnectionManager
from classes.FilesManager import FilesManager
import paramiko,time,os
import subprocess
from threading import Thread
from classes.KafkaLogger import KafkaLogger



class Experiment(Thread):

    output : dict

    def __init__(self, local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.compressionType = compressionType
        self.limit = limit
        self.remoteHostname = remoteHostname
        self.remoteUsername = remoteUsername
        self.remotePassword = remotePassword
        self.localPassword = localPassword
        self.streams = 1
        self.loggingId = loggingId
        self.logger = KafkaLogger()




    def clearRamCacheSwap(self,ssh,sftp):

        # Specify the desired working directory
        working_directory = '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration'

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
                        
    def runTransfer(self,stream):
        
        local_file_path = self.local_file_path
        remote_file_path = self.remote_file_path

        if stream != None:
            local_file_path = f"{self.local_file_path}_{stream:03d}"
            remote_file_path = f"{self.remote_file_path}_{stream:03d}"

        connectionManager = ConnectionManager(self.remoteHostname, self.remoteUsername, self.remotePassword,self.limit)
        try:
            connectionManager.connect()

        except paramiko.SSHException as sshException:
            print('Unable to establish SSH connection: %s' % sshException)
        except paramiko.SFTPError as sftpError:
            print('Unable to open SFTP session: %s' % sftpError)

        timeBeforeClear = time.time()
        self.clearRamCacheSwap(connectionManager.get_SSH(),connectionManager.get_SFTP())
        timeAfterClear = time.time()
        TotalClearTime = timeAfterClear - timeBeforeClear
        self.logger.log(self.loggingId,f"TotalClearTime : {TotalClearTime}, stream : {stream}")
        data = FilesManager.transferfile(connectionManager.get_SFTP(),local_file_path,remote_file_path,self.compressionType,self.limit,connectionManager.get_SSH(),self.loggingId)
        self.logger.log(self.loggingId,f"sizeOnTargetMachine : {data['sizeOnTargetMachine']}, stream : {stream}")
        self.logger.log(self.loggingId,f"sizeOnLocalMachine : {data['sizeOnTargetMachine']}, stream : {stream}")
        self.logger.log(self.loggingId,f"compressionTime : {data['compressionTime']}, stream : {stream}")
        self.logger.log(self.loggingId,f"dataTransferTime : {data['dataTransferTime']}, stream : {stream}")        
        self.logger.log(self.loggingId,f"readingFileTime : {data['readingFileTime']}, stream : {stream}")        
        data['TotalClearTime'] = TotalClearTime 
        connectionManager.close()
        return data