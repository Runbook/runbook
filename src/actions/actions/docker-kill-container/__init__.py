from fabric.api import env, run, hide
from ..utils import ShouldRun

def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    if ShouldRun(redata, jdata):
        env.gateway = redata['data']['gateway']
        env.host_string = redata['data']['host_string']
        env.user = redata['data']['username']
        env.key = redata['data']['sshkey']
        env.disable_known_hosts = True
        env.warn_only = True
        env.abort_on_prompts = True
        env.shell = "/bin/sh -c"
        cmd = ""
        if redata['data']['use_sudo'] == "true":
            cmd = "sudo "
        cmd = cmd + "docker kill {0}".format(redata['data']['container_name'])
        try:
            results = run_cmd(cmd)
            if results.succeeded:
                return True
            else:
                raise Exception(
                    'Command Execution Failed: {0} - {1}'.format(results.return_code, results))
        except:
            raise Exception(
                'Command failed to execute')

def run_cmd(cmd):
    with hide('output', 'running', 'warnings'):
        return run(cmd, timeout=1200)


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:  #pylint: disable=broad-except
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning(
            'docker-kill-container: Reaction {id} failed: {message}'.format(
                id=redata['id'], message=e.message))
        return False
