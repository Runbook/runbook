#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "-------------------------------------------------"
echo "Docker Environment:"
env
echo "-------------------------------------------------"
echo "[BOOTSTRAP] Generating config file"
cp /code/config/config.yml.example /config/config.yml
sed -i "s/28015/$DB_PORT_28015_TCP_PORT/" /config/config.yml
sed -i "s/rethink_host$/$DB_PORT_28015_TCP_ADDR/" /config/config.yml
sed -i "s/redis_ip$/$REDIS_PORT_6379_TCP_ADDR/" /config/config.yml
sed -i "s/3679/$REDIS_PORT_6379_TCP_PORT/" /config/config.yml
sed -i "s/6000/$ACTIONBROKER_PORT_6000_TCP_PORT/" /config/config.yml
sed -i "s/sink_host$/$ACTIONBROKER_PORT_6001_TCP_ADDR/" /config/config.yml
sed -i "s/6001/$ACTIONBROKER_PORT_6001_TCP_PORT/" /config/config.yml

echo "[BOOTSTRAP] Starting actioner.py"
python /code/actioner.py /config/config.yml
