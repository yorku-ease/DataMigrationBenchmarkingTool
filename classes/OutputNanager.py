import csv
from classes.OneStreamExperiment import OneStreamExperiment
from classes.MultipleStreamsExperiment import MultipleStreamsExperiment 
class OutputManager:

    def __init__(self,outputFilepath):
        
        self.outputFilepath = outputFilepath

        
    
    def writeCSVHeader(self, maximumNumberOfStreams):
        header = ['Experiment Number','file','stream', 'compressionType', 'limit' ,'totalTransferTime' , 'dataTransferTime', 'compressionTime', 'totalReadingFileTime','sizeOnLocalMachine','sizeOnTargetMachine']
        if maximumNumberOfStreams > 1 :
            for i in range(1, maximumNumberOfStreams+1 ):

                header.append('stream' + str(i) + 'totalTransferTime')
                header.append('stream' + str(i)+ 'dataTransferTime')
                header.append('stream' + str(i) + 'compressionTime')
                header.append('stream' + str(i) + 'totalReadingFileTime')


        with open(self.outputFilepath, 'w', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

        return
    
    def writeCSVContent(self, experiments : list[OneStreamExperiment] ):
        numberOfExperiments = len(experiments)
        AverageTotaltransferTime = 0 
        AverageDataTransferTime = 0
        AverageCompressionTime = 0
        AverageReadingFileTime = 0 
        for i in range(0,numberOfExperiments):
            data = experiments[i].getOutput()
            row = [i + 1 , experiments[i].getFilename(),"1",experiments[i].getCompressionType(),experiments[i].getLimit(),data['TotaltransferTime'], data['dataTransferTime'],data['compressionTime'], data['readingFileTime'], data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
            with open(self.outputFilepath, 'a', encoding='UTF8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
            AverageReadingFileTime += data['readingFileTime']/numberOfExperiments
            AverageTotaltransferTime += data['TotaltransferTime']/numberOfExperiments
            AverageDataTransferTime += data['dataTransferTime']/numberOfExperiments
            AverageCompressionTime += data['compressionTime']/numberOfExperiments


        row = ['average', experiments[i].getFilename(),"1",experiments[i].getCompressionType(),experiments[i].getLimit(),AverageTotaltransferTime, AverageDataTransferTime,AverageCompressionTime,AverageReadingFileTime, data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
        with open(self.outputFilepath, 'a', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)           
        
        return
    
#
