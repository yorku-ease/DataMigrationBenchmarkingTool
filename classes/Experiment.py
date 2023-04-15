from classes.ConnectionManager import ConnectionManager
from classes.FilesManager import FilesManager
import paramiko,time
import subprocess
      
class Experiment:

    output : dict

    def __init__(self, local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
        self.compressionType = compressionType
        self.limit = limit
        self.remoteHostname = remoteHostname
        self.remoteUsername = remoteUsername
        self.remotePassword = remotePassword
        self.localPassword = localPassword


    def clearRamCacheSwap(self,ssh):
        #clear RAM Cache as well as Swap Space at local machine

        output = subprocess.check_output([f"echo {self.localPassword} | ./clearcache.sh"],shell=True)
        print(output.decode("utf-8"))
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

    def runTransfer(self):
        print('before connection')
        connectionManager = ConnectionManager(self.remoteHostname, self.remoteUsername, self.remotePassword,self.limit)
        try:
            connectionManager.connect()

        except paramiko.SSHException as sshException:
            print('Unable to establish SSH connection: %s' % sshException)
        except paramiko.SFTPError as sftpError:
            print('Unable to open SFTP session: %s' % sftpError)
        print('before clear')

        timeBeforeClear = time.time()
        self.clearRamCacheSwap(connectionManager.get_SSH())
        timeAfterClear = time.time()
        TotalClearTime = timeAfterClear - timeBeforeClear
        print('before transfer')
        data = FilesManager.transferfile(connectionManager.get_SFTP(),self.local_file_path,self.remote_file_path,self.compressionType,self.limit,connectionManager.get_SSH())
        data['TotalClearTime'] = TotalClearTime
        print('afterTransfer')
        connectionManager.close()
        return data

