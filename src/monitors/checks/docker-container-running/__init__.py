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
    cmd = ""
    if jdata['data']['use_sudo'] == "true":
        cmd = "sudo "
    cmd = cmd + "docker inspect {0}".format(jdata['data']['container_name'])
    try:
        results = run_cmd(cmd)
    except:
        return None
    logger.debug("docker-container-running: requested command" +
                 " returned with exit code {0}".format(results.return_code))
    if results.succeeded:
        container_data = json.loads(results)
        if "State" not in container_data[0]:
            return False
        logger.debug("docker-container-running: container state" +
                     " returned running {0}".format(container_data[0]['State']['Running']))
        if container_data[0]['State']['Running']:
            return True
        else:
            return False
    else:
        return False
