import os,time,gzip,lz4.frame
class FilesManager:

    @staticmethod
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

    @staticmethod
    def removeSplittedFiles(input_file,num_files):
        # Loop through each splitted file in the directory
        for i in range(1,num_files + 1 ):
        # Check if the file exists and is a file (not a directory)
            if os.path.isfile(f"{input_file}_{i:03d}"):
                
                # Delete the file
                os.remove(f"{input_file}_{i:03d}")

    @staticmethod
    def progressCallback(transferred, total):
        percent = transferred / total * 100
        print(f'{transferred} bytes of the original file migrated ({percent:.2f}%)')
    
    @staticmethod
    def transferfile(sftp_client, localFilePath, remoteFilePath, compression, limit,ssh):
        compressionTime = 0
        dataTransferTime = 0
        readingFileTime = 0
        with open(localFilePath, "rb") as f:
            timeBeforeReadingFile = time.time()

            chunk=f.read(limit)
            remoteFilePath += "." + str(limit)

            if compression == "gzip":
                remoteFilePath +=  ".gz"
            elif compression == "lz4":
                remoteFilePath += ".lz4"
            


            transferred = 0
            sizeOnLocalMachine = os.stat(localFilePath).st_size
            sizeOnTargetMachine=0

            timeAfterReadingFile = time.time()
            readingFileTime += timeAfterReadingFile - timeBeforeReadingFile

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

                elif compression == 'None':
                    compressedChunk = chunk
                else :
                    print("Wrong compression type")
                    return 0
                
                sizeOnTargetMachine += len(compressedChunk)

                with sftp_client.open(remoteFilePath, 'ab') as outfile:
                    outfile.set_pipelined()
                    timeBeforeTransfer = time.time()
                    outfile.write(compressedChunk)
                    timeAfterTransfer = time.time()
                    dataTransferTime += timeAfterTransfer - timeBeforeTransfer


                transferred += len(chunk)
                FilesManager.progressCallback(transferred, sizeOnLocalMachine)
                chunk=f.read(limit)

            print(f'{sizeOnTargetMachine} bytes is the size of the file on the target Machine ')
            print(f'Compression took {compressionTime} seconds')
            print(f'Data Transfer took {dataTransferTime} seconds')
            data = {}

            data['readingFileTime'] = readingFileTime
            data['dataTransferTime'] = dataTransferTime
            data['compressionTime'] = compressionTime 
            data['sizeOnTargetMachine'] = sizeOnTargetMachine 
            data['sizeOnLocalMachine'] = sizeOnLocalMachine 

        return data