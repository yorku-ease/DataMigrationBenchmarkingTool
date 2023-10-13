
# Manual for using the data migration tool 

## Overview
A benchmarking tool that allows users to transfer files while compressing or decompressing them in real-time based on their preferences. The tool enables users to set transfer limits and generates a CSV report that displays the time taken for each step of the transfer process.

## Physical Requirements
- Source Server : 1 machine containing the files to be transferred.
- Target Server : 1 machine where the files are going to be migrated.
- Kafka Cluster : 1 machine to deploy the Kafka cluster to save all logs.


## Prerequisites
- Source server : Docker Compose must be installed on the machine.
- Target server : SSH must be enabled on the machine. 
- Kafka Cluster : Docker Compose & Python must be installed on the machine.


 ## Get Started

#### Configuration
<details><summary> Kafka Cluster</summary>
<br />
<p> 1. Download deployment/reporter.</p>
<p> 2. Edit deployment/reporter/kafka cluster/docker-compose.yml : <br/>
    &nbsp; &nbsp; In docker compose change these environment variables by changing 192.168.122.230 with your machine's public ip address.
    &nbsp; &nbsp; KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka1:19092,EXTERNAL://192.168.122.230:9092,DOCKER://host.docker.internal:29092
    &nbsp; &nbsp; KAFKA_JMX_HOSTNAME: 192.168.122.230</p>
<p>3. pip install -r deployment/reporter/requirements.txt </p>
</details>

<details><summary> Source Server</summary>

1. Download deployment/sourceserver
2. Save all files you want to migrate in deployment/sourceserver/data
3. Choose the right configuration for the experiment.
   <br />
   In this step, you'll edit the deployment/sourceserver/configs/config.ini file in the configs folder.

### **[remoteServer]**  
Here you save all SSH credentials of the remote server where to migrate the files

&nbsp; &nbsp; - **host** : hostname / IP address of the server<br />
&nbsp; &nbsp; - **username** : username of the server<br />
&nbsp; &nbsp; - **password** : password of the server<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files are going to be stored on the remote server <br /> 
&nbsp; &nbsp;( path should always end with / )<br />

### **[localServer]**  
The migration tool is going to be running on the localServer, But we need the password for this server  to run some sudo commands

&nbsp; &nbsp; - **password** : password to run sudo command<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files that are going to be migrated are savedb (path should always end with /).<br /> 
&nbsp; &nbsp;This value should always be data/ since you're saving your files in that folder as specified in step 1.
  
### **[experiment]** 


&nbsp; &nbsp; - **numberOfExperiments** : how many times each experiment is repeated with the same configuration ( for the accuracy of the results ).

&nbsp; &nbsp; - **files** = file1,file2,file3 :  only provide the names of the files. These files must be stored in the data folder specified above.

&nbsp; &nbsp; - **limits** = 1,10,1024 : limits should be in bytes 

&nbsp; &nbsp; - **compressionTypes** = None,lz4,gzip : compression types can be None, lz4 and gzip

 #### NOtE : all combinations of the 3 above variables will be executed as different experiments.


</details>

#### Running the experiment 
<details><summary> Step 3 : Run the experiment</summary>

Now everything is ready. 
Go to the root directory of the project and launch this command 
```docker

docker run --privileged --memory="0" --cpus="0" -v "$(pwd)"/data:/app/data -v "$(pwd)"/configs:/app/configs -v "$(pwd)"/output:/app/output fareshamouda/datamigrationbenchmarkingtool

```

this code will run the container with unlimited resources amd launch the experiment.
</details>

<details><summary> Step 4 : Result</summary>

The result of the experiment will be found in output folder in a CSV format file.

</details>
