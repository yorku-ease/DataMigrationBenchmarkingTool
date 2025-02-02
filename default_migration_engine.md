
# Default Migration Engine Documentation

This guide outlines the steps required to run DMBench with the **default migration engine**, which is used for general-purpose migrations. 
This file assumes you have already read the `README.md` file. Here, we will focus on steps from the **Configuration** section specific to the default migration engine. The rest of the process remains as described in the `README.md`.

If you want to extend the default migration engine, refer to the instructions in [`default_migration_engine_extend.md`](default_migration_engine_extend.md) before returning to this guide.

---

## Prerequisites

Before proceeding, ensure the following:

1. **Controller Machine Setup**:  
   - The **controller machine** must be the machine that contains the data to be transferred.  
   - This machine should have a folder with all the data you intend to migrate.  
   - Ensure that in the `inventory.ini` file in Ansible, the machine selected as the controller corresponds to this data-hosting machine.

## Configuration

In this section, we will guide you through **steps 3, 4, and 5** from the configuration section of the main README file. These steps are essential for setting up the Controller, configuring `docker-compose.yml`, and optionally using Ansible playbooks for the Default Migration Engine.

For detailed instructions on the other steps, please refer to the main README file.

Since the current engine is already supported, a significant portion of these steps is pre-configured.

### Step 3: Configuring the Controller

To configure the Controller for the Default Migration Engine, you will need to edit the following folder:

`deployment/controller/examples/defaultEngine`

### Configuration File: `configs/config.ini`

The file `configs/config.ini` needs to be configured as follows:

#### [targetServer]

- `host =` IP address of the target database  
- `username =` Username needed for connecting to the target database  
- `password =` Password needed for connecting to the target database  
- `dataFolder_path =` Absolute path of the folder where data needs to be saved

#### [sourceServer]

- `host =` IP address of the source database  
- `username =` Username needed for connecting to the source database  
- `password =` Password needed for connecting to the source database  
- `dataFolder_path = /app/data/` (do not change this)

#### [KafkaCluster]
#### This section needs to remain as it is not edited.
- `host = {{ hostvars["reporter"]["ansible_host"] }}` (don't change this)
- `port = 9092` (keep this as 9092)  
- `performanceBenchmarkTopic = performanceBenchmark`  
- `migrationEngineTopicName = migrationEngine`  
- `frameworktopicname = framework`  

#### [migrationEnvironment]

- `loggingId =` Leave empty for development purposes  
- `numberofexperiments =` Number of times the experiment will be repeated  
- `time_to_wait_beforeExperiment =` Number of seconds to sleep between experiments  
- `dummy = False` (keep this as False)

#### [experiment]

- `file =` The file(s) you would like to transfer each time, separated by commas (e.g., `file1.sql, file2.sql`)  
- `limit =` Limit of the size of the chunk to be read each time from the file in bytes  
- `compressiontype =` Compression type (None, gzip, or lz4)  
- `streams =` Number of parallel streams for migration

### Step 4: Setting up `docker-compose.yml`

For the  Default Migration Engine, nothing needs to be done here, as the Docker image is already dockerized, and the `docker-compose.yml` file is provided in the `configs` folder. You can use the pre-configured `docker-compose.yml` file for your migration engine setup.

However, the user is free to modify the resource constraints (such as CPU and RAM) in the `docker-compose.yml` file to experiment with different resource configurations. This allows you to test how the migration engine performs under various resource conditions.

### Step 5: Optional Ansible Playbooks for Migration Engines

For the Default Migration Engine, not much needs to be done here either. The necessary Ansible playbooks have already been implemented. These playbooks handle various stages of the migration process, including pre-experiment, starting the experiment, and post-experiment steps. You can refer to the playbooks in the `deployment/ansible/migrationengines/defaultEngine/` folder for more details.

In `deployment/ansible/migrationengines/defaultEngine/config.yml`, you need to specify the absolute path of the folder where data is stored on the controller machine. Make sure to provide the correct absolute path, as this will ensure the system can properly access and manage the data during the migration process.

### Final Steps

Once you have completed the configuration, you can now return to the [README.md](README.md) file. Follow the steps outlined there for running the experiment. 

Make sure to use the `default` tag when running the playbooks to ensure that the Default Migration Engine is properly utilized during the experiment.