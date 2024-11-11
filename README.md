
# Manual for using the data migration benchmarking tool 

## Overview
Welcome to DMBench – a versatile and scalable solution designed to streamline the process of data migration across diverse scenarios. This framework orchestrates the migration journey from a source machine to a target machine through a robust Controller and Migration Engine. Leveraging Docker containers for seamless deployment.

## Issues

If you encounter any issues or have questions while using our system, please don't hesitate to submit an issue on our GitHub repository.  Your contributions are crucial in improving the user experience.

## Tests

## Running Tests

To run tests for this project, please refer to the [TEST.md](TEST.md) file. The `TEST.md` file provides detailed instructions for each test scenario, including prerequisites, dependencies, and execution steps. Follow the outlined procedures to ensure the correctness and functionality of the project. If you encounter any issues or have questions related to the testing process, feel free to open an issue for assistance.

## Overview of Key Components

All the components of our framework, along with the data migration engine's environment, can be deployed either on a single machine, across separate machines, or a combination of both. The following descriptions will detail the role of each key component in the system.

### Data Migration Engine's Environment

These components are essential for the core data migration process and fall under the data migration engine's environment:

- **Data Source**: Where the data journey begins. The Migration Engine grabs data from here to send it off to the target machine.  
  *This is the origin point for the data migration.*
  
- **Data Target**: The final stop for migrated data. This is where data ends up after the Migration Engine does its job, finding its new home.  
  *This is the destination where the migrated data is placed.*

### Framework Environment

The following components support the framework, enabling management, tracking, and optimization of the migration process:

- **Controller**: The mastermind behind all experiments. It sets up the Migration Engine for each experiment, tweaking parameters. The Controller kicks off and oversees the migration, keeping an eye on performance through migration logs. It also tracks resource usage by using cAdvisor and node-exporter on the same setup as the migration engine.  
  *The Controller manages, configures, and monitors the entire migration process.*

- **Databases**: Two key players in the framework. Prometheus, the timeseries database, gathers resource data from cAdvisor. The second database is the home for all performance data from experiments. Prometheus focuses on resource metrics, while the second database stores broader performance data, making sure all experiment results are neatly organized.  
  *The two databases provide crucial data for tracking system performance and experiment results.*

- **Logs Reporter**: The organizer of experiment logs. It has two parts. The first part is a Kafka cluster, a storage space for all logs. Both the Controller and Migration Engine share their logs here, managed by a dedicated consumer. The second part is the parser. It not only extracts data from logs but also makes it easy for humans to read. Parsed info goes into CSV files before finding a permanent home in a NoSQL database. This two-part system ensures a smooth and effective process for handling, understanding, and gaining insights from experiment logs.  
  *The Logs Reporter manages, parses, and stores logs to facilitate insight extraction.*

## Prerequisites

To streamline the setup and deployment process, all key components of the framework are packaged as Docker containers. Each component has specific dependencies that must be installed on the machine where it will be deployed:

- **Controller & Migration Engine**: Requires Docker.
- **Logs Reporter**: Requires Docker and Python.
- **Databases**: Requires Docker.

While it's possible to deploy all components on a single machine, it is recommended to deploy them across separate machines, ideally in different locations. This setup mirrors real-world conditions, including network delays, which can help provide a more accurate evaluation of the migration process.


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
In this process, we will proceed step by step, emphasizing the importance of executing each component in a specified order. It is crucial to ensure that your source and target systems are operational and prepared for the migration process.

Let's begin systematically:

<details><summary> Databases</summary>
Start by initiating the databases.
  
   - On the Databases machine, change the current working directory to the databases folder.
   - Run the following command:
     ```bash
     docker-compose up
     ```
   - This will initiate `Prometheus` and `MongoDB` database along with `Grafana`. `Grafana` serves as a dashboard designed to help you monitor your migration engine's resource consumption in real-time.

</details>

<details><summary> Kafka Cluster</summary>
  Next, launch the Kafka cluster.
  
   - On the Kafka cluster machine, change the current working directory to the reporter/kafkacluster folder.
   - Run the following command:
     ```bash
     docker-compose up
     ```

</details>
 
<details><summary> Kafka Consumer</summary>
  After ensuring that Kafka is up and ready, follow up by activating the Kafka cluster's consumer.
  
   - On the Kafka cluster machine, change the current working directory to the reporter/kafkacluster folder.
   - Run the following command:
     ```bash
     python consumer.py
     ```
</details>
<details><summary> Controller</summary>
  
  Finally, initiate the Controller, which will orchestrate and commence all experiments.
  
   - On the controller machine, change the current working directory to the controller folder.
   - Run the following command:
     ```bash
     docker pull "<your migration engine image>"
     ```
     ```bash
     docker compose up
     ```
   - This will initiate the controller along with `cAdvisor` and `node-exporter`.
     - `cAdvisor` serves as a daemon that collects, aggregates, processes, and exports information about running the controller and the migration engine.
     - `node-exporter` is designed to monitor the host system where all the containers are deployed on.

</details>
<details><summary> Parser</summary>
  Upon completion of the experiment, indicated by the termination of the Controller container, it is essential to navigate to the Kafka cluster machine.
  
   - Subsequently, the parser needs to be executed. Throughout the experiment, resource consumption logs were promptly stored in Prometheus. However, the logs pertaining to performance benchmarks remain localized on the Kafka machine.
   - Running the parser becomes imperative at this juncture. Its role is twofold: to render the performance benchmark logs human-readable and to facilitate their exportation into `JSON` and `CSV` files. Furthermore, the parser ensures the archival of these logs in the `MongoDB` database for comprehensive analysis and reference.
   - On the Kafka cluster machine, change the current working directory to the reporter/logsParser folder.
   - Run the following command:
     ```bash
     python main.py
     ```
</details>

## Result

After following all the steps we talked about earlier, you've got a bunch of data from your experiments. Every performance benchmark, including migration time per experiment and, if there's any, compression time, is now neatly stored in the MongoDB database. At the same time, PrometheusDB has all the nitty-gritty details about resource consumption, and you can easily visualize it using the Grafana Dashboard. This mix ensures you've got all the important info at your fingertips for a deep dive into your experiments.

