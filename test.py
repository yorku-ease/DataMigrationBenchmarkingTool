import os 

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
    # Loop through each file in the directory
    for i in range(1,num_files + 1 ):
     # Check if the file exists and is a file (not a directory)
        if os.path.isfile(f"{input_file}_{i:03d}"):
            
            # Delete the file
            os.remove(f"{input_file}_{i:03d}")

#splitFile("data/test1.pdf",1)
#removeFiles("data/test1.pdf",1)