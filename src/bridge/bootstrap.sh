#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/config.yml.example /config/config.yml
sed -i "s/28015/$DB_PORT_28015_TCP_PORT/" /config/config.yml
sed -i "s/rethink_host$/$DB_PORT_28015_TCP_ADDR/" /config/config.yml
sed -i "s/redis_ip$/$REDIS_PORT_6379_TCP_ADDR/" /config/config.yml
sed -i "s/3679/$REDIS_PORT_6379_TCP_PORT/" /config/config.yml
sed -i "s/6000/$ACTIONBROKER_PORT_6000_TCP_PORT/" /config/config.yml
sed -i "s/sink_host$/$ACTIONBROKER_PORT_6001_TCP_ADDR/" /config/config.yml
sed -i "s/6001/$ACTIONBROKER_PORT_6001_TCP_PORT/" /config/config.yml

if [ -z "$1" ] ; then
    echo "[BOOTSTRAP] Running create_db.py"
    echo "-------------------------------------------------"
    python /code/mgmtscripts/create_db.py /config/config.yml
    if [ $? -eq 0 ] ; then
	echo "[BOOTSTRAP] Starting bridge.py"
	echo "-------------------------------------------------"
	python /code/bridge.py /config/config.yml
    else
	exit 1
    fi
else
    script="/code/mgmtscripts/$1"
    if [ -e "$script" ] ; then
	env python "$script" /config/config.yml
    else
	echo "Exiting: Cannot execute '$script'"
	exit 1
    fi
fi
