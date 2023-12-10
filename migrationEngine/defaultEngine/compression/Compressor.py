from abc import ABC, abstractmethod

class Compressor(ABC):

    @abstractmethod
    def compress(self,data)-> str:
        pass
    @abstractmethod
    def addFileExtension(self,filename)-> str:
        pass