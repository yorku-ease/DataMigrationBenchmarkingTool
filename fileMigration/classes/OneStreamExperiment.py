from classes.Experiment import Experiment


class OneStreamExperiment(Experiment):


    def runExperiment(self):
        data = self.runTransfer(stream=None)
        return data