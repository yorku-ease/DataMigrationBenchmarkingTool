import paramiko
import os
import gzip

print(paramiko.__version__)


def progress_callback(transferred, total):
    percent = transferred / total * 100
    print(f'{transferred} bytes transferred ({percent:.2f}%)')


def  transferfile(sftp_client, filepath, remotefilepath, compression, limit):
    with open(filepath, "rb") as f:
        chunk=f.read(limit)
        #only for testing this code will be updated later to check the fo the right compression 
        # current code only does gzip compression if needed
        if compression != None:
            remotefilepath += ".gz"

        while (chunk):
            if compression != None:
                chunk = gzip.compress(chunk)
            
            print(chunk)
            with sftp_client.open(remotefilepath, 'ab') as outfile:
                outfile.write(chunk)
           
            chunk=f.read(limit)

    return 0



# Enable logging
#logging.basicConfig(level=logging.INFO)

# Define the local file path
local_file_path = "data/test1.pdf"

# Define the remote file path
remote_file_path = "/home/" + os.environ.get('REMOTE1USERNAME') + "/test/te4tt10"

os.environ.get('REMOTE1HOSTNAME')


# Define the SSH parameters
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(os.environ.get('REMOTE1HOSTNAME'), username=os.environ.get('REMOTE1USERNAME'), password=os.environ.get('REMOTE1PASSWORD'))

# Open a SFTP connection
sftp = ssh.open_sftp()


transferfile(sftp_client=sftp,filepath=local_file_path,remotefilepath=remote_file_path,compression="gzip",limit=10)

# Close the SFTP connection
sftp.close()

# Close the SSH connection
ssh.close()