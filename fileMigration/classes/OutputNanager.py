import csv
from classes.Experiment import Experiment

from classes.OneStreamExperiment import OneStreamExperiment
from classes.MultipleStreamsExperiment import MultipleStreamsExperiment 
import logging
from confluent_kafka import Producer

logging.basicConfig(filename='/home/fareshamouda/DataMigrationBenchmarkingTool/fileMigration/output/output.log', level=logging.INFO ,filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class OutputManager:

    def __init__(self,outputFilepath):
        
        self.outputFilepath = outputFilepath
        self.producer = self.initkafkalogger()

        
    def initkafkalogger(self):
                # Define the Kafka broker(s) and topic name
        bootstrap_servers = "192.168.122.230:9092"  # Replace with your Kafka broker address
        self.topic_name = "my_topic"  # Replace with the Kafka topic you want to produce to

        # Create a Kafka producer instance
        producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'acks': 'all',  # Wait for all in-sync replicas to acknowledge
            'delivery.timeout.ms': 10000  # Set a delivery timeout (optional)
        })


        return producer
    def log(self,producer,message_key,message_value,topic_name):

        #producer.produce(topic=topic_name, key=message_key, value=message_value)
        return
    def terminatekafkalogger(self,producer):
        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

    def writeCSVHeader(self):
        header = ['Experiment Number',

                  'file',
                  'stream', 
                  'compressionType', 
                  'limit' ,
                  'totalTransferTime' , 
                  'TotalClearTime',
                  'dataTransferTime', 
                  'compressionTime', 
                  'totalReadingFileTime',
                  "sumReadingFileTime",
                  "maxReadingFileTime" ,
                  "avgReadingFileTime",
                  "sumDataTransferTime" ,
                  "maxDataTransferTime",
                  "avgDataTransferTime" ,
                  "sumCompressionTime" ,
                  "maxCompressionTime" ,
                  "avgCompressionTime",            
                  "sumTotalClearTime",
                  "maxTotalClearTime" ,
                  "avgTotalClearTime",
                  'sizeOnLocalMachine',
                  'sizeOnTargetMachine']
        
        """if maximumNumberOfStreams > 1 :
            for i in range(1, maximumNumberOfStreams+1 ):

                header.append('stream' + str(i) + 'totalTransferTime')
                header.append('stream' + str(i)+ 'dataTransferTime')
                header.append('stream' + str(i) + 'compressionTime')
                header.append('stream' + str(i) + 'totalReadingFileTime')

        """
        with open(self.outputFilepath, 'w', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

        return
    

    def writeCSVContent(self, experiments : list[Experiment] ):
        numberOfExperiments = len(experiments)
        AverageTotaltransferTime = 0 
        AverageDataTransferTime = 0
        AverageCompressionTime = 0
        AverageReadingFileTime = 0 
        AverageTotalClearTime = 0
        AverageSumReadingFileTime = 0
        AverageMaxReadingFileTime = 0
        AverageAvgReadingFileTime = 0
        AverageSumDataTransferTime = 0
        AverageMaxDataTransferTime = 0
        AverageAvgDataTransferTime = 0
        AverageSumCompressionTime = 0
        AverageMaxCompressionTime = 0
        AverageAvgCompressionTime = 0      
        AverageSumTotalClearTime = 0
        AverageMaxTotalClearTime = 0
        AverageAvgTotalClearTime = 0
        for i in range(0,numberOfExperiments):
            data = experiments[i].getOutput()
            streamsNumber = experiments[i].getStreamsNumber()
            if streamsNumber == 1 :
                row = [i + 1 , experiments[i].getFilename(),streamsNumber,experiments[i].getCompressionType(),experiments[i].getLimit(),data['TotaltransferTime'],data['TotalClearTime'], data['dataTransferTime'],data['compressionTime'], data['readingFileTime'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
            else :
                row = [i + 1 , experiments[i].getFilename(),streamsNumber,experiments[i].getCompressionType(),experiments[i].getLimit(),data['TotaltransferTime'],0, 0, 0, 0,  data["sumReadingFileTime"], data["maxReadingFileTime" ], data["avgReadingFileTime" ], data["sumDataTransferTime"] , data["maxDataTransferTime"] , data["avgDataTransferTime"] , data["sumCompressionTime"] , data["maxCompressionTime"] , data["avgCompressionTime"], data["sumTotalClearTime"] , data["maxTotalClearTime"] , data["avgTotalClearTime"] , data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]

            with open(self.outputFilepath, 'a', encoding='UTF8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
                logging.info(row)
                 # Produce a message to the Kafka topic
                message_key = "key1"  # Replace with your message key if needed
                message_value = str(row)  # Replace with your message content
                self.log(self.producer,message_key,message_value,self.topic_name)


            AverageTotaltransferTime += data['TotaltransferTime']/numberOfExperiments
            if streamsNumber == 1 :
                AverageReadingFileTime += data['readingFileTime']/numberOfExperiments
                AverageDataTransferTime += data['dataTransferTime']/numberOfExperiments
                AverageCompressionTime += data['compressionTime']/numberOfExperiments
                AverageTotalClearTime += data['TotalClearTime']/numberOfExperiments
            else :
                 AverageSumReadingFileTime += data['sumReadingFileTime']/numberOfExperiments
                 AverageMaxReadingFileTime += data['maxReadingFileTime']/numberOfExperiments
                 AverageAvgReadingFileTime += data['avgReadingFileTime']/numberOfExperiments
                 AverageSumDataTransferTime += data['sumDataTransferTime']/numberOfExperiments
                 AverageMaxDataTransferTime += data['maxDataTransferTime']/numberOfExperiments
                 AverageAvgDataTransferTime += data['avgDataTransferTime']/numberOfExperiments
                 AverageSumCompressionTime += data['sumCompressionTime']/numberOfExperiments
                 AverageMaxCompressionTime += data['maxCompressionTime']/numberOfExperiments
                 AverageAvgCompressionTime += data['avgCompressionTime']/numberOfExperiments         
                 AverageSumTotalClearTime += data['sumTotalClearTime']/numberOfExperiments
                 AverageMaxTotalClearTime += data['maxTotalClearTime']/numberOfExperiments
                 AverageAvgTotalClearTime += data['avgTotalClearTime']/numberOfExperiments

        if streamsNumber == 1 :
            row = ['average', experiments[i].getFilename(),streamsNumber,experiments[i].getCompressionType(),experiments[i].getLimit(),AverageTotaltransferTime,AverageTotalClearTime, AverageDataTransferTime,AverageCompressionTime,AverageReadingFileTime, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
        else :
            row = ['average', experiments[i].getFilename(),streamsNumber,experiments[i].getCompressionType(),experiments[i].getLimit(),AverageTotaltransferTime,0, 0, 0, 0, AverageSumReadingFileTime, AverageMaxReadingFileTime,AverageAvgReadingFileTime,AverageSumDataTransferTime,AverageMaxDataTransferTime,AverageAvgDataTransferTime,AverageSumCompressionTime,AverageMaxCompressionTime,AverageAvgCompressionTime,AverageSumTotalClearTime,AverageMaxTotalClearTime, AverageAvgTotalClearTime, data['sizeOnLocalMachine'], data['sizeOnTargetMachine']]
        with open(self.outputFilepath, 'a', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            logging.info(row)
            message_key = "key1"  # Replace with your message key if needed
            message_value = str(row)  # Replace with your message content
            self.log(self.producer,message_key,message_value,self.topic_name)
            writer.writerow(row)           
        
        self.terminatekafkalogger(self.producer)
        return
    def writeTotalExperimentTime(self, totalExperimentTime ):
        
        with open(self.outputFilepath, 'a', encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['total Experiment Time(hours)', totalExperimentTime])
