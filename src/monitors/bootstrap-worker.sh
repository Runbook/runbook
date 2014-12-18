#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "-------------------------------------------------"
echo "Docker Environment:"
env
echo "-------------------------------------------------"
echo "[BOOTSTRAP] Generating config file"
cp /code/config/worker.yml.example /config/config.yml
sed -i "s/5879/$MONITORBROKER_PORT_5879_TCP_PORT/" /config/config.yml
sed -i "s/broker_host$/$MONITORBROKER_PORT_5879_TCP_ADDR/" /config/config.yml
sed -i "s/5878/$MONITORBROKER_PORT_5878_TCP_PORT/" /config/config.yml
sed -i "s/sink_host$/$ACTIONBROKER_PORT_6000_TCP_ADDR/" /config/config.yml
sed -i "s/6000/$ACTIONBROKER_PORT_6000_TCP_PORT/" /config/config.yml

echo "[BOOTSTRAP] Starting worker.py"
python /code/worker.py /config/config.yml
