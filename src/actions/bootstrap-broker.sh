#!/bin/bash
## Docker Bootstrap Script

echo "Bootstrapping Application Environmental"
echo "-------------------------------------------------"
echo "Docker Environment:"
env
echo "-------------------------------------------------"
echo "[BOOTSTRAP] Generating config file"
cp /code/config/actionBroker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
python /code/broker.py /config/config.yml
