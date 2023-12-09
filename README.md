
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
For easy setup and deployment, all components of the framework are packaged as Docker containers. To run the tool, you'll need five machines, each with specific dependencies:
- Source Server
- Target Server
- Controller & Migration Engine: Docker
- Kafka Cluster: Docker, Python
- Databases: Docker
While it's possible to deploy everything on one machine, it's recommended to use separate machines, preferably in different locations. This setup adds a touch of realism to the migration process, accounting for potential network delays in the evaluation.

## Setting up the environment

In our Git repository, you'll find a dedicated deployment folder. Inside this folder, there are distinct subfolders—databases, controller, and reporter—each designed for download onto their respective machines.

## Configuration
In this section, we’ll configure each component of the framework deployed on each machine, assuming you’ve already downloaded the corresponding folders onto each machine.

<details><summary> Databases</summary>
<br />
For this machine, the only necessary configuration is to access the file `prometheus.yml` and modify the following sections by replacing 'localhost' with the IP address of the Controller & Migration Engine machine:

```yaml
- job_name: 'node-exporter'
  static_configs:
    - targets: ['<Controller-IP>:9100']

- job_name: 'cAdvisorr'
  static_configs:
    - targets: ['<Controller-IP>:9100']
```
Replace <Controller-IP> with the actual IP address of your Controller & Migration Engine machine. 

</details>

<details><summary> Kafka Cluster</summary>
<br />

For this machine, we have to configure two subfolders.

**Kafka Cluster**
1. Change the current working directory to the Kafka cluster folder.
2. Edit docker-compose.yml :
 <br/>  <br/>
   In docker compose change these environment variables by changing 192.168.122.145 with your machine's public ip address.
   KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka1:19092,EXTERNAL://192.168.122.145:9092,DOCKER://host.docker.internal:29092
   KAFKA_JMX_HOSTNAME: 192.168.122.145.
3. Run `pip install -r requirements.txt`.

**Logs Reporter**
1. Change the current working directory to the logsParser folder.
2. Open the file `config.ini`; you have to edit the following parameters:

   - `host = 192.168.122.1`: Change this with the IP address of your databases IP.
   - `user = root`: This is the default username used to run the NoSQL MongoDB. If you want to change it, you also have to change `MONGO_INITDB_ROOT_USERNAME` in `docker-compose.yml` on the databases machine.
   - `password = example`: This is the default password used to run the NoSQL MongoDB. If you want to change it, you also have to change `MONGO_INITDB_ROOT_PASSWORD` in `docker-compose.yml` on the databases machine.
</details>

<details><summary> Controller</summary>
<br />

The Controller utilizes a pivotal configuration file named "config.ini," crucial for providing essential settings to the Migration Engine. This configuration holds paramount importance, guiding users in the dockerization of their migration engine.

The "config.ini" file consists of two integral parts:

1. **First Part:**
   - This section is transmitted unaltered to the Migration Engine. Its content remains intact when creating `config.ini` for the migration engine.
  
   - **[[targetServer]]**
     - In this section, the user can put any information needed to connect to the target Server.
       - **host**
       - **user**
       - **password**
       
   - **[[sourceServer]]**
     - In this section, the user can put any information needed to connect to the source Server.
       - **host**
       - **user**
       - **password**
       
   - **[[KafkaCluster]]**
     - In this section, the user should only change the value of the IP address of the reporter machine. The other variables should remain with the default values.
       - **host**=192.168.122.143; this should be changed with the reporter IP
       - **port**=9092
       - **performanceBenchmarkTopic**=performanceBenchmark
       - **frameworkTopicName**=framework
       
   - **[[migrationEnvironment]]**
     - In this section, the user should choose to put information needed for the migration.
       - **migrationEngineDockerImage**: the name of the docker image the user created for the migration engine.
       - **loggingId**: In case the user needs all the logs and information collected during the monitoring to be assigned to a certain Id; this can be left empty.
       - **numberofexperiments**: how many times each experiment is repeated with the same configuration (for the accuracy of the results).

2. **Second Part:**
   - The second part encompasses all conceivable parameters for the migration scenarios users wish to evaluate. Each parameter combination is systematically chosen by the Controller, which then conveys these specific parameters to the Migration Engine one at a time.
   
   - **[[experiment]]**
     - In this section, this is an example for parameters for a file migration engine, the user can put parameters according to his engine.
       - **file** = file1.csv, file2.txt, file3.java
       - **limit** = 1048576, 1048576
       - **compressiontype** = None, gzip, lz4
       - **stream** = 3, 2, 1
       
   The Controller is responsible for examining all possible combinations when generating the configuration file for the Migration Engine. As an illustration of the second part of the configuration file, consider the following example:
   - **[[experiment]]**
     - **file** = file1.csv
     - **limit** = 1048576
     - **compressiontype** = None
     - **stream** = 3

</details>

## Dockerizing the migration engine

In this section, we delve into the migration engine Docker image as detailed in the configuration section . To effectively test your migration engine, adherence to our standards is essential. This implies dockerizing your migration engine in accordance with the specified guidelines.

For seamless execution, assume that the source and target of the data are already operational and prepared for migration when running the migration engine. Additionally, your Docker container should be configured to anticipate the configuration file generated by the Controller, as outlined in configuration section. Upon initiating the container, the migration process will commence.

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
