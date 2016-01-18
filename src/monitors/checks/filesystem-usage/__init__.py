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
    cmd = "df"
    try:
        results = run_cmd(cmd)
    except:
        return None
    logger.debug("filesystem-usage: requested command" +
                 " returned with exit code {0}".format(results.return_code))
    if results.succeeded:
        lines = results.splitlines()
        fs_stats = {}
        # Extract filesystem mount point and usage
        for line in lines[1:]:
            data = line.split()
            fs_stats[data[-1]] = int(data[-2].rstrip("%"))
    else:
        return None

    threshold = int(jdata['data']['threshold'])
    file_system = jdata['data']['file_system']

    # Check for specific filesystem usage
    if file_system in fs_stats.keys():
        if fs_stats[file_system] < threshold:
            return True
        else:
            logger.debug("filesystem-usage: file system {0} above threshold".format(
                file_system))
            return False

    # Check for all file systems
    for fs in fs_stats.keys():
        if fs_stats[fs] > threshold:
            logger.debug("filesystem-usage: file system {0} above threshold".format(fs))
            return False
    return True
