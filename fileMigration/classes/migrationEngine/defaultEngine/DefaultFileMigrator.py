from classes.migrationEngine.FileMigrator import FileMigrator 
from classes.migrationEngine.defaultEngine.ConnectionManager import ConnectionManager 
from classes.migrationEngine.defaultEngine.filesmanager.FilesManager import FilesManager 
import paramiko,subprocess,time,threading
import concurrent.futures



class DefaultFileMigrator(FileMigrator):

    def __init__(self,remoteHostname, remoteUsername, remotePassword,localPassword,loggingId,logger = None):
        self.localPassword = localPassword
        self.remoteHostname = remoteHostname
        self.remotePassword = remotePassword
        self.remoteUsername = remoteUsername
        self.logger = logger
        self.loggingId = loggingId


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

        connectionManager = self.connect()
        ssh = connectionManager.get_SSH()
        sftp = connectionManager.get_SFTP()

        
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
        connectionManager.close()

    def migrate(self,local_file_path,remote_file_path,compressionType,limit,streams):

        timeBeforeClear = time.time()
        self.clearRamCacheSwap()
        timeAfterClear = time.time()
        TotalClearTime = timeAfterClear - timeBeforeClear
        self.logger.log(self.loggingId,f"TotalClearTime : {TotalClearTime}")
        
        if streams == 1 :
            data = self.migrateOneStream(local_file_path,remote_file_path,compressionType,limit)
        else:
            data = self.migrateMultipleStreams(local_file_path,remote_file_path,compressionType,limit,streams)
        return data
            

    def migrateOneStream(self,local_file_path,remote_file_path,compressionType,limit):
        

        connectionManager = self.connect()
        ssh = connectionManager.get_SSH()
        sftp = connectionManager.get_SFTP()

        data = FilesManager.transferfile(sftp,local_file_path,remote_file_path,compressionType,limit,ssh,self.loggingId)
        threadName = threading.current_thread().name
        if threadName == "MainThread":
            streamNumber = None
        else:
            streamNumber = int(threadName.split("_")[1]) + 1
        connectionManager.close()
        self.logger.log(self.loggingId,f"sizeOnTargetMachine : {data['sizeOnTargetMachine']}, stream : {streamNumber}")
        self.logger.log(self.loggingId,f"sizeOnLocalMachine : {data['sizeOnTargetMachine']}, stream : {streamNumber}")
        self.logger.log(self.loggingId,f"compressionTime : {data['compressionTime']}, stream : {streamNumber}")
        self.logger.log(self.loggingId,f"dataTransferTime : {data['dataTransferTime']}, stream : {streamNumber}")        
        self.logger.log(self.loggingId,f"readingFileTime : {data['readingFileTime']}, stream : {streamNumber}")   
        return data
    
    def migrateMultipleStreams(self,local_file_path,remote_file_path,compressionType,limit,streams):
        
        filesmanager = FilesManager 

        filesmanager.splitFile(local_file_path,streams)
        local_chunks_paths,remote_chunks_paths = filesmanager.getChunksPaths(local_file_path,remote_file_path,streams)
        max_threads = streams

        # Create a ThreadPoolExecutor with the specified number of threads
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:

            # Submit tasks to the pool with parameters
            for i in range(len(local_chunks_paths)):
                slocal_file_path = local_chunks_paths[i]
                sremote_file_path = remote_chunks_paths[i]
                executor.submit(self.migrateOneStream, slocal_file_path,sremote_file_path,compressionType,limit)
        
        # Shut down the executor and wait for all tasks to finish
        executor.shutdown(wait=True)

        filesmanager.removeSplittedFiles(local_file_path,streams)