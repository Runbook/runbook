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
            cmd = "sysctl vm.stats.vm.v_free_count vm.stats.vm.v_page_size vm.stats.vm.v_page_count"
            results = run_cmd(cmd)
            if results.succeeded:
                memstats = {}
                for line in results.splitlines():
                    line_data = line.split()
                    key = line_data[0].rstrip(":")
                    memstats[key] = int(line_data[1])
                free_mem = memstats['vm.stats.vm.v_free_count'] * \
                           memstats['vm.stats.vm.v_page_size']
                total_mem = memstats['vm.stats.vm.v_page_count'] * \
                            memstats['vm.stats.vm.v_page_size']
            else:
                return None
        else:
            cmd = "cat /proc/meminfo"
            results = run_cmd(cmd)
            if results.succeeded:
                memstats = {}
                for line in results.splitlines():
                    line_data = line.split()
                    key = line_data[0].rstrip(":")
                    memstats[key] = int(line_data[1])
                if "MemAvailable" in memstats:
                    free_mem = memstats['MemAvailable']
                else:
                    ## Linux Memory Calculation
                    free_mem = (memstats['MemFree'] - memstats['Buffers']) + memstats['Cached']
                total_mem = memstats['MemTotal']
            else:
                return None
    else:
        return None

    logger.debug("free-memory: Total Memory {0} Free Memory {1} ".format(total_mem, free_mem))
    free_perc = float(free_mem) / float(total_mem)
    threshold = float(jdata['data']['threshold']) / 100
    logger.debug("free-memory: Free Percent {0} Threshold {1}".format(free_perc, threshold))
    if free_perc >= threshold:
        return True
    else:
        return False
