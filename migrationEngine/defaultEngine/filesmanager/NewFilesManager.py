from classes.migrationEngine.defaultEngine.filesmanager.FilesManager import FilesManager
from typing import List, Tuple

class NewFilesManager(FilesManager):

    
    @staticmethod
    def splitFile(input_file,num_files = None):
        #this function takes input_file which is the full path of the file and splits it into chunks and saves them in the data folder
        #it's preferable to use input_file to choose the path of the chunks.
        #you might optionally give it num_files if you want to specify how many chunks you want to save
        pass
    @staticmethod
    def getChunksPaths(local_file_path,remote_file_path,num_files = None)-> Tuple[List[str], List[str]]:
        #local_file_path is the full path of the file without split
        #remote_file_path is the full path of the file without split on the remote machine , this is useful to choose the remote_chunks_paths
        #this function returns local_chunks_paths which are the paths of the chunks after running splitFile 
        # and remote_chunks_paths which should be the paths of the chunks on the remote machine 
        pass
    @staticmethod
    def removeSplittedFiles(input_file,num_files= None):
        #this function deletes the local chunks after migrating them
        #this function can stay empty if you prefer to keep the local chunks
        pass