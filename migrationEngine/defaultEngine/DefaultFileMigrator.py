from ConnectionManager import ConnectionManager 
from filesmanager.FilesManager import FilesManager 
import paramiko,subprocess,time,threading
import concurrent.futures



class DefaultFileMigrator():

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
    


    def migrate(self,local_file_path,remote_file_path,compressionType,limit,streams):
        
        if streams == 1 :
            data = self.migrateOneStream(local_file_path,remote_file_path,compressionType,limit)
        else:
            data = self.migrateMultipleStreams(local_file_path,remote_file_path,compressionType,limit,streams)
        return data
            

    def migrateOneStream(self,local_file_path,remote_file_path,compressionType,limit):
        threadName = threading.current_thread().name
        if threadName == "MainThread":
            streamNumber = None
        else:
            streamNumber = int(threadName.split("_")[1]) + 1

        self.logger.logMigrationEngine(self.loggingId,f"type : info, migration : started, Timestamp : {time.time()}, stream : {streamNumber}")
        connectionManager = self.connect()
        ssh = connectionManager.get_SSH()
        sftp = connectionManager.get_SFTP()


        FilesManager.transferfile(sftp,local_file_path,remote_file_path,compressionType,limit,ssh,self.loggingId,streamNumber)

        connectionManager.close()
        self.logger.logMigrationEngine(self.loggingId,f"type : info, migration : completed, Timestamp : {time.time()}, stream : {streamNumber}")

    
    def migrateMultipleStreams(self,local_file_path,remote_file_path,compressionType,limit,streams):
        filesmanager = FilesManager
        self.logger.logMigrationEngine(self.loggingId,f"type : info, fileSplitting : started, Timestamp : {time.time()}")
        filesmanager.splitFile(local_file_path,streams)
        self.logger.logMigrationEngine(self.loggingId,f"type : info, fileSplitting : completed, Timestamp : {time.time()}")
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