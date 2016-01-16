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
            cmd = "swapinfo"
            results = run_cmd(cmd)
            if results.succeeded:
                lines = results.splitlines()
                swapinfo = lines[1].split()
                total_swap = int(swapinfo[1])
                used_swap = int(swapinfo[2])
            else:
                return None
        else:
            cmd = "cat /proc/meminfo"
            results = run_cmd(cmd)
            if results.succeeded:
                swapstats = {}
                for line in results.splitlines():
                    line_data = line.split()
                    key = line_data[0].rstrip(":")
                    swapstats[key] = int(line_data[1])
                total_swap = swapstats['SwapTotal']
                used_swap = swapstats['SwapTotal'] - swapstats['SwapFree']
            else:
                return None
    else:
        return None

    logger.debug("swap-used: Total Swap {0} Swap Used {1} ".format(total_swap, used_swap))
    if total_swap == 0:
        # avoid dividing by zero
        return True
    used_perc = float(used_swap) / float(total_swap)
    threshold = float(jdata['data']['threshold']) / 100
    logger.debug("swap-used: Used Percent {0} Threshold {1}".format(used_perc, threshold))
    if used_perc < threshold:
        return True
    else:
        return False
