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
cp /code/config/actionBroker.yml.example /config/config.yml

echo "-------------------------------------------------"
echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml
