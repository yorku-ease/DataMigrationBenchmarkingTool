# DB2 Migration Service Documentation

## Overview
This repository contains the source code for the Docker image `fareshamouda/db2migrationservice`. The image provides an environment tailored for DB2 migration tasks and is built on IBM's Migration Platform.

## Building the Image

### Prerequisites
1. **IBM Migration Platform**: To build your own image, you must download the appropriate version of `ibm_db2bridge_platform-1.1.0.el8.x86_64.rpm.tar` from the IBM Early Access Program.
2. **Red Hat Subscription**: A valid Red Hat subscription is required for the build process. You will need your Red Hat subscription username and password.

### Build Instructions
To build the image locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Download the `ibm_db2bridge_platform-1.1.0.el8.x86_64.rpm.tar` file, uncompress it, and place the `RPMS` folder in the project directory, next to the `Dockerfile`.

3. Run the Docker build command with the necessary build arguments:
   ```bash
   docker build -t fareshamouda/db2migrationservice:debug . \
     --build-arg REDHAT_USERNAME=<your_redhat_username> \
     --build-arg REDHAT_PASSWORD=<your_redhat_password>
   ```

### Build Arguments
- `REDHAT_USERNAME`: Your Red Hat subscription username.
- `REDHAT_PASSWORD`: Your Red Hat subscription password.

Ensure that these arguments are correctly provided to successfully authenticate with the Red Hat repositories during the build process.

## Contributing
Contributions are welcome! However, please note the following:
- You are responsible for obtaining and downloading the required `ibm_migration_platform-BETA5-rhel8` file through IBM’s Early Access Program.
- Ensure that your contributions comply with the licensing and usage terms of the IBM Migration Platform and Red Hat.

## Support
If you encounter any issues or have questions about this project, please open an issue in this repository or contact the maintainer.
