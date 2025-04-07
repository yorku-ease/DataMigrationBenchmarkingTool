#! /usr/bin/bash


export LANG=en_US.UTF-8
su - migplat -c 'db2bridge_server &' 

export WEBSITE_PASSWORD=$(crudini --get /app/configs/migrationEngineConfig.ini migrationEnvironment websitePassword) 
export WEBSITE_USERNAME=$(crudini --get /app/configs/migrationEngineConfig.ini migrationEnvironment websiteUsername)


echo -e "1\n$WEBSITE_USERNAME\n$WEBSITE_PASSWORD\n\n\n\n\n" | db2bridge_setup
echo -e "$WEBSITE_PASSWORD" | su - migplat -c 'db2bridge_start'




sleep 30
if lsof -i :14080 > /dev/null; then
  echo "✅ Website is running on port 14080."
else
  echo "❌ Website is not listening on port 14080."
fi

python3 main.py

#tail -f /dev/null