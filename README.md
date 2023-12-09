
# Manual for using the data migration benchmarking tool 

## Overview
A benchmarking tool that allows users to transfer files while compressing or decompressing them in real-time based on their preferences. The tool enables users to set transfer limits and generates a CSV report that displays the time taken for each step of the transfer process.
If you want to extend our tool follow this [manual](EXTEND.md)

## Physical Requirements
- Source Machine: Where the data journey begins. The Migration Engine grabs data from here to send it off to the target machine.
- Target Machine: The final stop for migrated data. This is where data ends up after the Migration Engine does its job, finding its new home.
- Controller: The mastermind behind all experiments. It sets up the Migration Engine for each experiment, tweaking parameters. The Controller kicks off and oversees the migration, keeping an eye on performance through migration logs. It also tracks resource usage by using cAdvisor and node-exporter on the same setup as the migration engine.
- Databases: Two key players in the framework. Prometheus, the timeseries database, gathers resource data from cAdvisor. The second database is the home for all performance data from experiments. Prometheus focuses on resource metrics, while the second database stores broader performance data, making sure all experiment results are neatly organized.
- Logs Reporter: The organizer of experiment logs. It has two parts. The first part is a Kafka cluster, a storage space for all logs. Both the Controller and Migration Engine share their logs here, managed by a dedicated consumer. The second part is the parser. It not only extracts data from logs but also makes it easy for humans to read. Parsed info goes into CSV files before finding a permanent home in a NoSQL database. This two-part system ensures a smooth and effective process for handling, understanding, and gaining insights from experiment logs.


## Prerequisites
- Source server : Docker Compose must be installed on the machine.
- Target server : SSH must be enabled on the machine. 
- Kafka Cluster : Docker Compose & Python must be installed on the machine.

## Configuration
<details><summary> Kafka Cluster</summary>
<br />
<p> 1. Download deployment/reporter.</p>
<p> 2. Edit deployment/reporter/kafka cluster/docker-compose.yml :
 <br/>  <br/>
   In docker compose change these environment variables by changing 192.168.122.230 with your machine's public ip address.
   KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka1:19092,EXTERNAL://192.168.122.230:9092,DOCKER://host.docker.internal:29092
   KAFKA_JMX_HOSTNAME: 192.168.122.230.</p>
<p>3. pip install -r deployment/reporter/requirements.txt </p>
</details>

<details><summary> Source Server</summary>
<br />
<p>1. Download deployment/sourceserver</p>
<p>2. Save all files you want to migrate in deployment/sourceserver/data</p>
<p>3. Choose the right configuration for the experiment.
   <br />
   In this step, you'll edit the deployment/sourceserver/configs/config.ini file in the configs folder.

### **[targetServer]**  
Here you save all SSH credentials of the remote server where to migrate the files

&nbsp; &nbsp; - **host** : hostname / IP address of the server<br />
&nbsp; &nbsp; - **username** : username of the server<br />
&nbsp; &nbsp; - **password** : password of the server<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files are going to be stored on the remote server <br /> 
&nbsp; &nbsp;( path should always end with / )<br />

### **[sourceServer]**  
The migration tool is going to be running on the localServer, But we need the password for this server  to run some sudo commands

&nbsp; &nbsp; - **password** : password to run sudo command<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files that are going to be migrated are savedb (path should always end with /).<br /> 
&nbsp; &nbsp;This value should always be data/ since you're saving your files in that folder as specified in step 1.
  
### **[KafkaCluster]**  
The migration tool is going to be running on the localServer, But we need the password for this server  to run some sudo commands

&nbsp; &nbsp; - **host** :  hostname / IP address of the machine hosting the kafka cluster<br />
&nbsp; &nbsp; - **port** :  the port on which the kafka cluster is listening ; the value should be 9092<br /> 
  

### **[experiment]** 


&nbsp; &nbsp; - **numberOfExperiments** : how many times each experiment is repeated with the same configuration ( for the accuracy of the results ).

&nbsp; &nbsp; - **files** = file1,file2,file3 :  only provide the names of the files. These files must be stored in the data folder specified above.

&nbsp; &nbsp; - **limits** = 1,10,1024 : limits should be in bytes 

&nbsp; &nbsp; - **compressionTypes** = None,lz4,gzip : compression types can be None, lz4 and gzip

&nbsp; &nbsp; - **streams** = 1,2,3 : the number of streams that files will be migrated over

&nbsp; &nbsp; - **logginId** =  : Id used when logging everything about experiments, if kept empty a new id will be created

 #### Note : all combinations of the 3 above variables will be executed as different experiments.
</p>
</details>

## Running the experiment 
<details><summary> Kafka Cluster</summary>

<br />
<p> 1. Change Directory ; use the 'cd' command to change your working directory to deployment/reporter/kafka cluster.</p>
<p> 2. Run docker compose up </p>
<p> 3. Wait until kafka cluster is up and ready. </p>
<p> 4. Run python consumer.py. </p>
NOTE: if this is not the first time running the experiment, don't forget to delete logs saved in deployment/reporter/kafka cluster/output.log, if you don't want to see the logs of the old experiments in the final result.
</details>

<details><summary> Target Server</summary>
<br />
<p> 1. Make sure SSH server is ready for connections.</p>
<p> 2. Make sure there is enough space on the machine.</p>
</details>
 
<details><summary> Source Server</summary>
<br />
<p> 1. Change Directory ; use the 'cd' command to change your working directory to deployment/sourceserver.</p>
<p> 2. Run docker compose up </p>
<p> Now you can follow the experiments running ; you can follow the output in the source server and you can also see the logs of  consumer.py in the Kafka cluster</p>
</details>

## Result
<p> 1. Change Directory ; use the 'cd' command to change your working directory to deployment/reporter/logsParser. </p>
<p> 4. Run python main.py </p>

Now you'll find data.json and data.csv in logsParser folder containing all becnhmarks of the experiments.
