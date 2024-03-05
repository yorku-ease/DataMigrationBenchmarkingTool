from compression.compressor import Compressor
import gzip
class GzipCompressor(Compressor):

    
    def compress(self,data):
        return gzip.compress(data)
    def addFileExtension(self,filename):
        return filename + ".gz"