import os,time,threading
from kafkaLogger import KafkaLogger
from compression.gzipCompressor import GzipCompressor
from compression.lz4Compressor import Lz4Compressor


class FilesManager:

    @staticmethod
    def splitFile(input_file,num_files = None):
        
        Totalnum_files = num_files
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
                output_file = f"{input_file}_{Totalnum_files}_{file_num:03d}"
                
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
    def getChunksPaths(local_file_path,remote_file_path,num_files = None):
        local_chunks_paths =[]
        remote_chunks_paths =[]
        for i in range(1,num_files +1 ):
            local_chunks_paths.append(f"{local_file_path}_{num_files}_{i:03d}")
            remote_chunks_paths.append(f"{remote_file_path}_{num_files}_{i:03d}")
        return local_chunks_paths,remote_chunks_paths
        

    @staticmethod
    def removeSplittedFiles(input_file,num_files=None):
        # Loop through each splitted file in the directory
        for i in range(1,num_files + 1 ):
        # Check if the file exists and is a file (not a directory)
            if os.path.isfile(f"{input_file}_{num_files}_{i:03d}"):
                
                # Delete the file
                os.remove(f"{input_file}_{num_files}_{i:03d}")

    @staticmethod
    def progressCallback(transferred, total):
        percent = transferred / total * 100
        current_thread = threading.current_thread()
        print("Thread", current_thread.name)
        print(f'{transferred} bytes of the original file migrated ({percent:.2f}%)')
    
    @staticmethod
    def transferfile(sftp_client, localFilePath, remoteFilePath, compression, limit,ssh,loggingId,streamNumber):
        logger = KafkaLogger()
        compressionTime = 0
        dataTransferTime = 0
        readingFileTime = 0
        with open(localFilePath, "rb") as f:
            logger.logMigrationEngine(loggingId,f"type : info, ReadingFile : started, Timestamp : {time.time()}, stream : {streamNumber}")

            timeBeforeReadingFile = time.time()

            chunk=f.read(limit)
            remoteFilePath += "." + str(limit)

            if compression == "gzip":
                compressor = GzipCompressor()
            elif compression == "lz4":
                compressor = Lz4Compressor()
            elif compression == "None":
                pass
            else:
                print("Wrong compression type")
                return 0
            
            if compression != 'None':
                remoteFilePath = compressor.addFileExtension(remoteFilePath)


            transferred = 0
            sizeOnLocalMachine = os.stat(localFilePath).st_size
            sizeOnTargetMachine=0

            timeAfterReadingFile = time.time()
            readingFileTime += timeAfterReadingFile - timeBeforeReadingFile
            logger.logMigrationEngine(loggingId,f"type : info, ReadingFile : completed, Timestamp : {time.time()}, stream : {streamNumber}")

            i = 0 
            while (chunk):
                i += 1 
                if compression == 'None':
                    compressedChunk = chunk
                else:
                    logger.logMigrationEngine(loggingId,f"type : info, FileChunk{i} : started, Timestamp : {time.time()}, stream : {streamNumber}")
                    timeBeforeCompression = time.time()
                    compressedChunk = compressor.compress(chunk)
                    timeAfterCompression = time.time()
                    compressionTime += timeAfterCompression - timeBeforeCompression
                    logger.logMigrationEngine(loggingId,f"type : info, FileChunk{i} : completed, Timestamp : {time.time()}, stream : {streamNumber}")


                
                sizeOnTargetMachine += len(compressedChunk)
                logger.logMigrationEngine(loggingId,f"type : info, FileChunk{i}Transfer : started, Timestamp : {time.time()}, stream : {streamNumber}")
                with sftp_client.open(remoteFilePath, 'ab') as outfile:
                    outfile.set_pipelined()
                    timeBeforeTransfer = time.time()
                    outfile.write(compressedChunk)
                    timeAfterTransfer = time.time()
                    dataTransferTime += timeAfterTransfer - timeBeforeTransfer
                logger.logMigrationEngine(loggingId,f"type : info, FileChunk{i}Transfer : completed, Timestamp : {time.time()}, stream : {streamNumber}")


                transferred += len(chunk)
                FilesManager.progressCallback(transferred, sizeOnLocalMachine)
                chunk=f.read(limit)
            current_thread = threading.current_thread()
            print("Thread", current_thread.name)
            print(f'{sizeOnTargetMachine} bytes is the size of the file on the target Machine ')
            print(f'Compression took {compressionTime} seconds')
            print(f'Data Transfer took {dataTransferTime} seconds')
            logger.logPerformanceBenchmark(loggingId,f"sizeOnTargetMachine : {sizeOnTargetMachine}, stream : {streamNumber}")
            logger.logPerformanceBenchmark(loggingId,f"sizeOnLocalMachine : {sizeOnTargetMachine}, stream : {streamNumber}")
            logger.logPerformanceBenchmark(loggingId,f"compressionTime : {compressionTime}, stream : {streamNumber}")
            logger.logPerformanceBenchmark(loggingId,f"dataTransferTime : {dataTransferTime}, stream : {streamNumber}")        
            logger.logPerformanceBenchmark(loggingId,f"readingFileTime : {readingFileTime}, stream : {streamNumber}")   