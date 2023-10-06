from classes.migrationEngine.FileMigrator import FileMigrator 
from classes.migrationEngine.defaultEngine.ConnectionManager import ConnectionManager 
from classes.migrationEngine.defaultEngine.FilesManager import FilesManager 
from classes.migrationEngine.defaultEngine.ThreadStream import ThreadStream 
import paramiko,subprocess

class DefaultFileMigrator(FileMigrator):

    def __init__(self,remoteHostname, remoteUsername, remotePassword,localPassword,loggingId):
        self.localPassword = localPassword
        self.remoteHostname = remoteHostname
        self.remotePassword = remotePassword
        self.connectionManager = ConnectionManager(remoteHostname, remoteUsername, remotePassword)

        self.loggingId = loggingId
        try:
            self.connectionManager.connect()

        except paramiko.SSHException as sshException:
            print('Unable to establish SSH connection: %s' % sshException)
        except paramiko.SFTPError as sftpError:
            print('Unable to open SFTP session: %s' % sftpError) 
        self.ssh = self.connectionManager.get_SSH()
        self.sftp = self.connectionManager.get_SFTP()

    def clearRamCacheSwap(self):

        # Specify the desired working directory
        #working_directory = '/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration'

        # Change the current working directory
        #os.chdir(working_directory)
        # Copy the file to the remote machine
        #self.sftp.put("clearcache.sh", "clearcache.sh")

        
        #clear RAM Cache as well as Swap Space at local machine
        result = subprocess.run([f"echo {self.localPassword} | ./clearcache.sh"], stdout=subprocess.PIPE, shell=True)
        # Print the output of the command
        print(result.stdout.decode('utf-8'))

        #output = subprocess.check_output([f"echo {self.localPassword} | ./clearcache.sh"],shell=True)
        #print(output.decode("utf-8"))
        print("On local machine")
        #clear RAM Cache as well as Swap Space at remote machine

        stdin, stdout, stderr = self.ssh.exec_command(f"echo {self.remotePassword} | ./clearcache.sh")
        output = stdout.read().decode("utf-8")

        # Print output 
        print(output)
        print("On remote machine")

    def migrate(self,local_file_path,remote_file_path,compressionType,limit):
        data = self.migrateOneStream(local_file_path,remote_file_path,compressionType,limit)
        return data
            

    def migrateOneStream(self,local_file_path,remote_file_path,compressionType,limit):
        data = FilesManager.transferfile(self.sftp,local_file_path,remote_file_path,compressionType,limit,self.ssh,self.loggingId)
        return data
    
    def migrateMultipleStreams(self,local_file_path,remote_file_path,compressionType,limit,streams):
        threads = []
        

        FilesManager.splitFile(local_file_path,streams)

        for i in range(1,streams +1 ):
            #output_file = f"{input_file}_{file_num:03d}"
            thread = ThreadStream(target=self.migrateOneStream, stream=i)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        pass
        
    def shutdown(self):
        self.connectionManager.close()