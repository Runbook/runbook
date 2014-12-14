python src/web/web.py instance/web.cfg.default &
python src/monitors/control.py src/monitors/config/control.yml.5min.default &
python src/monitors/broker.py src/monitors/config/main.yml.default &
python src/monitors/worker.py src/monitors/config/main.yml.default &
python src/bridge/bridge.py src/bridge/config/config.yml.default &
python src/actions/broker.py src/bridge/config/config.yml.default &
python src/actions/actioner.py src/actions/config/config.yml.default &