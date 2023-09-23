#!/bin/bash
docker compose  -f "/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/docker-compose.yml" down

source_container_name="source"
target_container_name="target"
sourcedatadir="/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/sourcedatadir"
targetdatadir="/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/targetdatadir"
rootpassword=$USERPASSWORD


if [ ! -d "$sourcedatadir" ]; then
   mkdir "$sourcedatadir"
else
echo "$rootpassword" | su -c "rm -fr "$sourcedatadir"/*" root
fi

if [ ! -d "$targetdatadir" ]; then
    mkdir "$targetdatadir"
else

echo "$rootpassword" | su -c "rm -fr "$targetdatadir"/*" root

fi

docker compose -f "/home/fareshamouda/DataMigrationBenchmarkingTool/databaseMigration/docker-compose.yml" up -d



state=$(docker inspect -f '{{ .State.Health.Status }}' ${source_container_name})

while [ "$(docker inspect -f '{{ .State.Health.Status }}' ${source_container_name})" != "healthy" ]; do
    echo "Waiting for container source to be ready..."
    sleep 5

done

echo "Source database is ready for connections"

docker exec -it "source" mysql -u root  -e "source /tmp/mysqlsampledatabase.sql"


echo "Sample database imported to source database"

while [ "$(docker inspect -f '{{ .State.Health.Status }}' ${target_container_name})" != "healthy" ]; do
    echo "Waiting for container target to be ready..."
    sleep 5
done

echo "Target database is ready for connections"

