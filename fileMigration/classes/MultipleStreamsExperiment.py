from classes.Experiment import Experiment

from classes.ThreadStream import ThreadStream
from classes.FilesManager import FilesManager


class MultipleStreamsExperiment(Experiment):
    def __init__(self, local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword,streams, loggingId):

        super().__init__(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId)
        self.streams = streams
        self.data = None

    def runExperiment(self):
        #use threads
        threads = []
        
        maxReadingFileTime=0
        sumReadingFileTime=0

        maxDataTransferTime=0
        sumDataTransferTime=0

        maxCompressionTime=0
        sumCompressionTime=0

        maxTotalClearTime=0
        sumTotalClearTime=0    

        sizeOnTargetMachine=0
        sizeOnLocalMachine=0
        FilesManager.splitFile(self.local_file_path,self.streams)

        for i in range(1,self.streams +1 ):
            #output_file = f"{input_file}_{file_num:03d}"
            thread = ThreadStream(target=self.runTransfer, stream=i)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            data = thread.join()


            sumReadingFileTime += data['readingFileTime']
            sumDataTransferTime += data['dataTransferTime']
            sumCompressionTime += data['compressionTime']
            sumTotalClearTime += data['TotalClearTime']

            maxReadingFileTime = max(maxReadingFileTime,data['readingFileTime'])
            maxDataTransferTime = max(maxDataTransferTime, data['dataTransferTime'])
            maxCompressionTime = max(maxCompressionTime,data['compressionTime'])
            maxTotalClearTime = max(maxTotalClearTime,data['TotalClearTime'])

            sizeOnLocalMachine += data['sizeOnLocalMachine']
            sizeOnTargetMachine += data['sizeOnTargetMachine']
        
        avgReadingFileTime = sumReadingFileTime / self.streams
        avgDataTransferTime = sumDataTransferTime / self.streams
        avgCompressionTime = sumCompressionTime / self.streams
        avgTotalClearTime= sumTotalClearTime / self.streams
        

        result = {
            "sumReadingFileTime" : sumReadingFileTime,
            "maxReadingFileTime" : maxReadingFileTime,
            "avgReadingFileTime" : avgReadingFileTime,
            "sumDataTransferTime" : sumDataTransferTime,
            "maxDataTransferTime" : maxDataTransferTime,
            "avgDataTransferTime" : avgDataTransferTime,
            "sumCompressionTime" : sumCompressionTime,
            "maxCompressionTime" : maxCompressionTime,
            "avgCompressionTime" : avgCompressionTime,            
            "sumTotalClearTime" : sumTotalClearTime,
            "maxTotalClearTime" : maxTotalClearTime,
            "avgTotalClearTime" : avgTotalClearTime,

            "sizeOnTargetMachine" : sizeOnTargetMachine,
            "sizeOnLocalMachine" : sizeOnLocalMachine
        }
        
        return result