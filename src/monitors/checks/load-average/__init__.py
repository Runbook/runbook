from fabric.api import hide, run, env
import time
import json

def run_cmd(cmd):
    with hide('output', 'running', 'warnings'):
        return run(cmd, timeout=1200)

def check(**kwargs):
    ''' Login over SSH and execute shell command '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']

    env.gateway = jdata['data']['gateway']
    env.host_string = jdata['data']['host_string']
    env.user = jdata['data']['username']
    env.key = jdata['data']['sshkey']
    env.shell = "/bin/sh -c"
    env.disable_known_hosts = True
    env.warn_only = True
    env.abort_on_prompts = True
    results = run_cmd("uptime")
    if results.succeeded:
        data = results.split()
        load = float(data[-3].rstrip(","))
    else:
        return None

    logger.debug("load-average: 1 minute load average is {0}".format(load))
    if load < float(jdata['data']['threshold']):
        return True
    else:
        return False
