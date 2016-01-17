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
    sudo = ""
    if jdata['data']['use_sudo'] == "true":
        sudo = "sudo"
    service = jdata['data']['service_name']
    try:
        results = run_cmd("{0} service {1} status".format(sudo, service))
    except:
        return None
    if results.succeeded and "running" in results:
        return True
    else:
        try:
            results = run_cmd("{0} systemctl status {1}".format(sudo, service))
        except:
            return None
        if results.succeeded:
            return True
        else:
            return False
