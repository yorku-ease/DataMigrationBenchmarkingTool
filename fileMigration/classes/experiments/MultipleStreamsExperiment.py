from classes.experiments.Experiment import Experiment

from classes.experiments.ThreadStream import ThreadStream
from classes.migrationEngine.defaultEngine.FilesManager import FilesManager


class MultipleStreamsExperiment(Experiment):
    def __init__(self, local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword,streams, loggingId):

        super().__init__(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword, loggingId)
        self.streams = streams
        self.data = None

    def runExperiment(self):
        #use threads
        threads = []
        

        FilesManager.splitFile(self.local_file_path,self.streams)

        for i in range(1,self.streams +1 ):
            #output_file = f"{input_file}_{file_num:03d}"
            thread = ThreadStream(target=self.runTransfer, stream=i)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
