import paramiko,os


hostname = os.environ.get('REMOTE1HOSTNAME')
username = os.environ.get('REMOTE1USERNAME')
password = os.environ.get('REMOTE1PASSWORD')



transport = paramiko.Transport((hostname, 22))
transport.connect(username = username, password = password)

#sftp = paramiko.SFTPClient.from_transport(transport)

# create an SSH client object using the transport
ssh = paramiko.SSHClient()
ssh._transport = transport
