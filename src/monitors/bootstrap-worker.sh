#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "-------------------------------------------------"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env
echo "-------------------------------------------------"
echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/worker.yml.example /config/config.yml
sed -i "s/5879/$MONITORBROKER_PORT_5879_TCP_PORT/" /config/config.yml
sed -i "s/broker_host$/$MONITORBROKER_PORT_5879_TCP_ADDR/" /config/config.yml
sed -i "s/5878/$MONITORBROKER_PORT_5878_TCP_PORT/" /config/config.yml
sed -i "s/sink_host$/$ACTIONBROKER_PORT_6000_TCP_ADDR/" /config/config.yml
sed -i "s/6000/$ACTIONBROKER_PORT_6000_TCP_PORT/" /config/config.yml

echo "-------------------------------------------------"
echo "[BOOTSTRAP] Starting worker.py"
echo "-------------------------------------------------"
python /code/worker.py /config/config.yml
