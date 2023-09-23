#!/bin/bash
docker compose down 


if [ ! -d "sourcedatadir" ]; then
    mkdir "sourcedatadir"
else
sudo rm -fr datadir/*
fi

if [ ! -d "targetdatadir" ]; then
    mkdir "targetdatadir"
else

sudo rm -fr targetdatadir/*
fi

docker compose up -d
#docker run --name="$container_name" \
#--mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/my.cnf,dst=/etc/my.cnf \
#--mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/datadir,dst=/var/lib/mysql \
#--mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/sampledata/mysqlsampledatabase.sql,dst=/tmp/mysqlsampledatabase.sql \
#-e MYSQL_ALLOW_EMPTY_PASSWORD=true \
#-e MYSQL_ROOT_HOST:"%" \
#-p 3306:3306 \
#-d container-registry.oracle.com/mysql/community-server:8.0.32 


log_phrase="ready for connections"
while ! docker logs "source" 2>&1 | grep -q "$log_phrase"; do
    echo "Waiting for container source to be ready..."
    sleep 5
done

sleep 10


docker exec -it "source" mysql -u root  -e "source /tmp/mysqlsampledatabase.sql"

backup_name=$(date +%s)
backup_name+="all-databases.sql"

sleep 10


docker run --entrypoint "/bin/sh" --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/sourcedatadir,dst=/var/lib/mysql --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0.32 \
-c "mysqldump -u root -p --all-databases > /data/backups/"$backup_name""

#diff backups/1687571519all-databases.sql <(ssh remote1 "cat /home/casuser/data/1687571519all-databases.sql.104857600")

#docker exec -it "$container_name" bash -c 'mysql -u root  <   /tmp/mysqlsampledatabase.sql'

#Percona XtraBackup

/bin/python3.9 /home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/migration.py

rm -f /home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/source.sql
rm -f /home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/target.sql

docker run --entrypoint "/bin/sh" --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/sourcedatadir,dst=/var/lib/mysql --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0.32 \
-c "mysqldump --skip-comments --skip-extended-insert -u root -p classicmodels > /data/backups/source.sql"

docker run --entrypoint "/bin/sh" --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/targetdatadir,dst=/var/lib/mysql --mount type=bind,src=/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/backups/,dst=/data/backups \
--rm container-registry.oracle.com/mysql/community-server:8.0.32 \
-c "mysqldump --skip-comments --skip-extended-insert -u root -p classicmodels > /data/backups/target.sql"

diff backups/source.sql backups/target.sql