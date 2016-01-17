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
    results = run_cmd("uname -a")
    if results.succeeded:
        if "FreeBSD" in results:
            cmd = "vmstat 2 2"
            results = run_cmd(cmd)
            if results.succeeded:
                lines = results.splitlines()
                vmstat_info = lines[-1].split()
                cpu_idle = float(vmstat_info[-1])
            else:
                return None
        else:
            cmd = "vmstat 2 2"
            results = run_cmd(cmd)
            if results.succeeded:
                lines = results.splitlines()
                vmstat_info = lines[-1].split()
                cpu_idle = float(vmstat_info[-3])
            else:
                return None
    else:
        return None

    threshold = float(jdata['data']['threshold'])
    logger.debug("cpu-idle: Idle {0} Threshold {1}".format(cpu_idle, threshold))
    if cpu_idle > threshold:
        return True
    else:
        return False
