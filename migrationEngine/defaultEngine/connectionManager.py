import paramiko
class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)


class ConnectionManager:

    def __init__(self, hostname,username,password):
        # Define the SSH parameters
        self.hostname = hostname
        self.username = username
        self.password = password

    def connect(self):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, username=self.username, password = self.password)
        #ssh.get_transport().window_size = self.limit
        self.ssh = ssh
        # Open a SFTP connection
        self.sftp = self.ssh.open_sftp()
        

    def get_SSH(self):
        return self.ssh

    def get_SFTP(self):
        return self.sftp
    def close_SFTP(self):
        self.sftp.close()
    
    def close(self):
        self.close_SFTP()
        self.ssh.close()
