#THIS FILE IS DEPRECATED CHECK MAIN.PY
























import paramiko
import os
import gzip
import lz4.frame
import time
import csv
import subprocess

# Notes
# add streams 
# use conf file
# change the value of sleep for test

def progress_callback(transferred, total):
    percent = transferred / total * 100
    print(f'{transferred} bytes of the original file migrated ({percent:.2f}%)')

def splitFile(input_file,num_files):
    
    # Open the input file for reading in binary mode
    with open(input_file, 'rb') as f_in:
        
        # Determine the size of the input file in bytes
        file_size = os.path.getsize(input_file)
        
        # Determine the size of each output file in bytes
        split_size = file_size // num_files
        
        # Initialize the file counter
        file_num = 1
        
        # Read the input file in chunks of split_size bytes
        while True:
            chunk = f_in.read(split_size)
            
            # If the chunk is empty, we have reached the end of the file
            if not chunk:
                break
            
            # Define the output file name
            output_file = f"{input_file}_{file_num:03d}"
            
            # Open the output file for writing in binary mode
            with open(output_file, 'wb') as f_out:
                
                # Write the chunk to the output file
                f_out.write(chunk)
            
            # Increment the file countercd 
            file_num += 1
            
            # Decrease the number of remaining files
            num_files -= 1
            
            if num_files == 0:
                break
            # Recalculate the split size for the remaining files
            split_size = (file_size - f_in.tell()) // num_files


def removeFiles(input_file,num_files):
    # Loop through each splitted file in the directory
    for i in range(1,num_files + 1 ):
     # Check if the file exists and is a file (not a directory)
        if os.path.isfile(f"{input_file}_{i:03d}"):
            
            # Delete the file
            os.remove(f"{input_file}_{i:03d}")


def  transferfile(sftp_client, filepath, remotefilepath, compression, limit):
    compressionTime = 0
    dataTransferTime = 0
    with open(filepath, "rb") as f:
        
        chunk=f.read(limit)
        remotefilepath += "." + str(limit)

        if compression == "gzip":
            remotefilepath +=  ".gz"
        elif compression == "lz4":
            remotefilepath += ".lz4"
        


        transferred = 0
        sizeOnLocalMachine = os.stat(filepath).st_size
        sizeOnTargetMachine=0

        
        while (chunk):
            if compression == "gzip":
                timeBeforeCompression = time.time()
                compressedChunk = gzip.compress(chunk)
                timeAfterCompression = time.time()
                compressionTime += timeAfterCompression - timeBeforeCompression

            elif compression == "lz4":
                timeBeforeCompression = time.time()
                compressedChunk = lz4.frame.compress(chunk)
                timeAfterCompression = time.time()
                compressionTime += timeAfterCompression - timeBeforeCompression

            elif compression == None:
                compressedChunk = chunk
            else :
                print("Wrong compression type")
                return 0
            

            sizeOnTargetMachine += len(compressedChunk)
            with sftp_client.open(remotefilepath, 'ab') as outfile:
                timeBeforeTransfer = time.time()
                print("hi")
                outfile.write(compressedChunk)
                print("hi2")
                timeAfterTransfer = time.time()
                dataTransferTime += timeAfterTransfer - timeBeforeTransfer


            transferred += len(chunk)
            progress_callback(transferred, sizeOnLocalMachine)

            chunk=f.read(limit)

        print(f'{sizeOnTargetMachine} bytes is the size of the file on the target Machine ')
        print(f'Compression took {compressionTime} seconds')
        print(f'Data Transfer took {dataTransferTime} seconds')
        data = {}
        data['dataTransferTime'] = dataTransferTime
        data['compressionTime'] = compressionTime 
        data['sizeOnTargetMachine'] = sizeOnTargetMachine 
        data['sizeOnLocalMachine'] = sizeOnLocalMachine 

    return data

def ss(local_file_path,file,stream,remote_file_path,numberOfExperiments,ssh,sftp,compressionType,limit):
    AverageTotaltransferTime = 0 
    AverageDataTransferTime = 0
    AverageCompressionTime = 0
    for i in range(0,numberOfExperiments):
        clearRamCacheSwap(ssh)
        timeBeforeTransfer = time.time()
        data = transferfile(sftp_client=sftp,filepath=local_file_path,remotefilepath=remote_file_path,compression=compressionType,limit=limit)
        timeAfterTransfer = time.time()
        TotaltransferTime = timeAfterTransfer - timeBeforeTransfer
        #rearrange row to become more readable
        row = [i + 1 , file,stream,compressionType,limit,TotaltransferTime, data['dataTransferTime'],data['compressionTime'], data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
        with open('output/output2.csv', 'a', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        AverageTotaltransferTime += TotaltransferTime/numberOfExperiments
        AverageDataTransferTime += data['dataTransferTime']/numberOfExperiments
        AverageCompressionTime += data['compressionTime']/numberOfExperiments
        print("Sleeping for 5 minutes...")

      #  time.sleep(300)
        print("Woke up!")
    #insert the row with average values after all rows of each experiment
    row = ['average', file,stream,compressionType,limit,AverageTotaltransferTime, AverageDataTransferTime,AverageCompressionTime, data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
    with open('output/output2.csv', 'a', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)            
 

def clearRamCacheSwap(ssh):
    #clear RAM Cache as well as Swap Space at local machine
    output = subprocess.check_output(["echo $USERPASSWORD | ./clearcache.sh"],shell=True)

    print(output.decode("utf-8"))
    print("On local machine")
    #clear RAM Cache as well as Swap Space at remote machine

    remotePassword = os.environ.get('REMOTE1PASSWORD')
    stdin, stdout, stderr = ssh.exec_command(f"echo {remotePassword} | ./clearcache.sh")
    output = stdout.read().decode("utf-8")

    # Print output 
    print(output)
    print("On remote machine")



# Enable logging
#logging.basicConfig(level=logging.INFO)

# Define the path of the folder containing data files 
local_DataFolder_path = "data/"

# Define the remote file path
remote_DataFolder_path = "/home/" + os.environ.get('REMOTE1USERNAME') + "/data/"

os.environ.get('REMOTE1HOSTNAME')


# Define the SSH parameters
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(os.environ.get('REMOTE1HOSTNAME'), username=os.environ.get('REMOTE1USERNAME'), password=os.environ.get('REMOTE1PASSWORD'))



# Open a SFTP connection
sftp = ssh.open_sftp()
streams = [1]
files = ["DS_001.csv"]
#100 Mib and 200 Mib
#add function that converts Mib,kib,gib to bytes
limits = [1024*1024*1024]
compressionTypes = [None,"gzip"]
numberOfExperiments = 2
#rearrange header to become more readable
header = ['Experiment Number','file','stream', 'compressionType', 'limit', 'totalTransferTime' , 'dataTransferTime', 'compressionTime','sizeOnLocalMachine','sizeOnTargetMachine']
with open('output/output2.csv', 'w', encoding='UTF8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

for file in files:
    for limit in limits:
        for compressionType in compressionTypes:
            for stream in streams:
                local_file_path = local_DataFolder_path + file
                remote_file_path = f"{remote_DataFolder_path}{file}"
                #splitFile(local_file_path,stream)
                
                #for i in range(1,stream + 1 ):
                # Check if the file exists and is a file (not a directory)
                    #local_file_path = f"{local_DataFolder_path + file}_{i:03d}"
                    #remote_file_path = f"{remote_DataFolder_path}{file}_{i:03d}"
                ss(local_file_path,file,stream,remote_file_path,numberOfExperiments,ssh,sftp,compressionType,limit)
                # implement a callback function that each time takes the thread's result an saves data in output.csv and then calculate the average
                # use an array to save averages of all streams and after all experiments we save the average 
                # take the loop for experiments numer outside of ss()
                # change cleaning Ram and Swap
                # add classes 
                # remove ssh and sftp
                # avoid hard coding
                # change readme 
                # 1st loop to create experiments object
                # 2nd run simulations

                
# Close the SFTP connection
sftp.close()

# Close the SSH connection
ssh.close()

