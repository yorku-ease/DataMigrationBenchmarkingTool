from classes.Experiment import Experiment
import threading

class MultipleStreamsExperiment(Experiment):
    def __init__(self, local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword,streams):

        super().__init__(local_file_path, remote_file_path, compressionType, limit, remoteHostname, remoteUsername, remotePassword, localPassword)
        self.streams = streams

    def runExperiment(self):
        #use threads
        threads = []
        for i in range(1,self.streams +1 ):
            thread = threading.Thread(target=self.runTransfer)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        #change this later 
        # get data from each thread and then write the output to csv file 
        return