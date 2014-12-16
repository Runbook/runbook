import subprocess

TEXT_FILE = 'pid.txt'
DATA = []


def run_web():
    pipe = subprocess.Popen(
        ['python', 'src/web/web.py', 'instance/web.cfg.default'])
    DATA.append(pipe.pid)


def run_monitors_controller():
    pipe = subprocess.Popen(
        ['python', 'src/monitors/control.py',
            'src/monitors/config/control.yml.5min.default'])
    DATA.append(pipe.pid)


def run_monitors_broker():
    pipe = subprocess.Popen(
        ['python', 'src/monitors/broker.py',
            'src/monitors/config/control.yml.5min.default'])
    DATA.append(pipe.pid)


def run_monitors_worker():
    pipe = subprocess.Popen(
        ['python', 'src/monitors/worker.py',
            'src/monitors/config/main.yml.default'])
    DATA.append(pipe.pid)


def run_bridge():
    pipe = subprocess.Popen(
        ['python', 'src/bridge/bridge.py',
            'src/bridge/config/config.yml.default'])
    DATA.append(pipe.pid)


def run_actions_broker():
    pipe = subprocess.Popen(
        ['python', 'src/actions/broker.py',
            'src/actions/config/config.yml.default'])
    DATA.append(pipe.pid)


def run_actions_actioner():
    pipe = subprocess.Popen(
        ['python', 'src/actions/actioner.py',
            'src/bridge/config/config.yml.default'])
    DATA.append(pipe.pid)


def add_to_text_file():
    with open(TEXT_FILE, "wt") as f:
        for entity in DATA:
            f.write("{0}\n".format(entity))


def main():
    run_web()
    run_monitors_controller()
    run_monitors_broker()
    run_monitors_worker()
    run_bridge()
    run_actions_broker()
    run_actions_actioner()
    add_to_text_file()


if __name__ == '__main__':
    main()
