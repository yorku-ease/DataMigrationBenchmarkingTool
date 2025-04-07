
# DB2 Bridge Documentation

## Overview

This document outlines the steps needed to run **DMBench** with the **DB2 Bridge**, which is specifically designed for migrating DB2 databases.  

This file assumes that you have already read the main [README.md](README.md). Here, we will focus on some specific configurations for the DB2 Bridge. All other steps remain as described in the README file.

---

## Prerequisites

Before proceeding, ensure the following:

1. **Databases Setup**:  
   - A **source database** and a **target database** must be up and running. These will serve as the origin and destination for the DB2 migration process.  
   - The **source database** should already contain the data you want to transfer.  
   - The machines must have been started with Docker Compose, and there should be a Docker Compose file for each database on their respective machines. This setup will ensure that both the source and target DB2 databases are properly configured to run with Docker Compose, making it easier to test experiments with resource constraints on the machines.

2. **Dummy Table Option**:  
   - `dummy = True` (Set to `True` if you want to run a dummy experiment before each combination of parameters, not before all experiments, just the first one to override the cache)  
   - `dummyTable =` Name of the table to be migrated during the dummy experiment (ensure `dummy` is set to `True`).  Ideally, this should be a table different from the ones you intend to migrate.

## Configuration

In this section, we will guide you through **steps 3, 4, and 5** from the configuration section of the main README file. These steps are essential for setting up the Controller, configuring `docker-compose.yml`, and optionally using Ansible playbooks for the DB2 Bridge. 

For detailed instructions on the other steps, please refer to the main README file.

Since the current engine is already supported, a significant portion of these steps is pre-configured.

### Step 3: Configuring the Controller

To configure the Controller for the DB2 Bridge, you will need to edit the following folder:

`deployment/controller/examples/db2`

### Configuration File: `configs/config.ini`

The file `configs/config.ini` needs to be configured as follows:

#### [targetServer]

- `host =` IP address of the target database  
- `username =` Username needed for connecting to the target database  
- `password =` Password needed for connecting to the target database  
- `port =` Port of the target database  
- `type = db2` or `cloud` (use `db2` for local databases or `cloud` for DB2 on cloud)

#### [sourceServer]

- `host =` IP address of the source database  
- `username =` Username needed for connecting to the source database  
- `password =` Password needed for connecting to the source database  
- `port =` Port of the source database  

#### [KafkaCluster]

#### This section needs to remain as it is not edited.
- `host =` {{ hostvars["reporter"]["ansible_host"] }} 
- `port = 9092` (Keep this as the default port for the reporter)  
- `performanceBenchmarkTopic = performanceBenchmark` (Keep this as default)  
- `migrationEngineTopicName = migrationEngine` (Keep this as default)  
- `frameworkTopicName = framework` (Keep this as default)

#### [migrationEnvironment]

- `loggingId =` (Leave it empty for development purposes, can be left blank)  
- `numberofexperiments =` (Specify how many times each combination of parameters should be repeated)  
- `time_to_wait_beforeExperiment =` Number of seconds to wait before each experiment starts  
- `dummy = False` (Set to `True` if you want to run a dummy experiment before each combination of parameters, not before all experiments, just the first one to override the cache)  
- `dummyTable =` Name of the table to be migrated during the dummy experiment (ensure `dummy` is set to `True`)

#### [experiment]

This section contains the parameters for the migration experiments.

- `compress =` LZ4, gzip, or none (Choose the compression type for migration)  
- `sourceDatabasetoTargetDatabase =` `test_test` (The name of the source and target databases, separated by an underscore)  
- `tables =` LINEITEM (List the tables you want to migrate, separate multiple tables with underscores)  
- `maxStreams =` Maximum number of parallel streams for the migration  
- `binary =` False or True (Set to True to enable binary migration)
- `websiteUsername = ` admin (This is the username for the website started by IBM Bridge. Keep this as default, but you can change it if needed) 
- `websitePassword = ` EWeBBqOF8LwcHDQI (This is the password for the website started by IBM Bridge. Keep this as default, but you can change it if needed)

### Configuration File: `configs/migrationengine_static.json`

This file contains more advanced configuration settings for the IBM Bridge. You can edit these settings to customize the behavior of the migration engine, or you can choose to keep the default values if no changes are needed.

### Step 4: Setting up `docker-compose.yml`

For the DB2 Bridge, nothing needs to be done here, as the Docker image is already dockerized, and the `docker-compose.yml` file is provided in the `configs` folder. You can use the pre-configured `docker-compose.yml` file for your migration engine setup.

However, the user is free to modify the resource constraints (such as CPU and RAM) in the `docker-compose.yml` file to experiment with different resource configurations. This allows you to test how the migration engine performs under various resource conditions.



### Step 5: Optional Ansible Playbooks for Migration Engines

For the DB2 Bridge, not much needs to be done here either. The necessary Ansible playbooks have already been implemented. These playbooks handle various stages of the migration process, including pre-experiment, starting the experiment, and post-experiment steps. You can refer to the playbooks in the `deployment/ansible/migrationengines/db2/` folder for more details.

However, there are a couple of important tasks to complete:

1. **Configure `inventory.ini` for DB2 Machines**

   Go to `deployment/ansible/inventory.ini` and add two machines for your DB2 migration:

   - `db2-targetDB`
   - `db2-sourceDB`

   Make sure the management server has access to both of these machines by configuring their details in the inventory file.

2. **Configure Docker Compose for Databases**  
This section is optional. You can have your databases up and running wherever you want (on-premises or in the cloud). However, if you want to use the steps that handle the deployment and monitor the resource consumption of the DB2 databases, follow the instructions below:

To use these steps, you need to:
1. Add the `check_db2_DBs` tag to your playbook runs.
2. Ensure that the Docker Compose files are present in the `deployment/ansible/migrationengines/db2/databases` directory.  
3. Make sure to name the service for the source database `db2source` and the service for the target database `db2target` in the Docker Compose files. Additionally, add container names for both of these services.

Both the source and target DB2 databases should be started using the configured Docker Compose files. These files must also be appropriately configured on the source and target DB2 machines. This setup ensures that DMBench can manage and adjust the resources (CPU, RAM, etc.) allocated to these databases as needed.

Before each experiment, DMBench will verify that the Docker Compose files in `deployment/ansible/migrationengines/db2/databases` match the databases currently running on the respective source and target machines. If discrepancies are found, DMBench will stop the old databases and start new ones using the updated resource allocations. This ensures consistent and accurate testing conditions.

Additionally, the steps will automatically pull and run **cAdvisor** on the machines where the databases are hosted. cAdvisor will monitor and log the resource consumption (CPU, memory, etc.) of both the source and target databases. This provides valuable insights into database performance and helps ensure proper resource allocation during experiments.

In `deployment/ansible/migrationengines/db2/config.yml`, you need to specify the folder paths (without a trailing slash `/` at the end) where these Docker Compose files exist on each machine. Update the configuration with the correct paths so that the management server can manage the Docker Compose services for both databases and monitor their resource consumption.


### Final Steps

Once you have completed the configuration, you can now return to the [README.md](README.md) file. Follow the steps outlined there for running the experiment. 

Make sure to use the `db2` tag when running the playbooks to ensure that the DB2 migration engine is properly utilized during the experiment.

