from abc import ABC, abstractmethod

class FileMigrator(ABC):

    @abstractmethod
    def __init__(self,remoteHostname, remoteUsername, remotePassword,localPassword,loggingId=None,logger = None):
        pass

    @abstractmethod
    def clearRamCacheSwap():
        pass
    @abstractmethod
    def migrate(self,local_file_path,remote_file_path,compressionType,limit,loggingId):
        pass
