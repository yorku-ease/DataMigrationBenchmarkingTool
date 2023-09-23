#!/bin/bash

backup_name=$1
sourcedatadirPath=$2
backupsFolderPath=$3

docker run --entrypoint "/bin/sh" --mount type=bind,src=$sourcedatadirPath,dst=/var/lib/mysql --mount type=bind,src=$backupsFolderPath,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0.32 \
-c "mysqldump -u root -p --all-databases > /data/backups/"$backup_name""

