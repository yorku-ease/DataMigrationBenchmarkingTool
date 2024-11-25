from compression.compressor import Compressor
import lz4.frame
class Lz4Compressor(Compressor):
    
    def compress(self,data):
        return lz4.frame.compress(data)
    def addFileExtension(self,filename):
        return filename + ".lz4"