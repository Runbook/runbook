"""DigitalOcean - Create new droplet reaction."""

import json
import requests
import time

_HTTP_TIMEOUT = 10.0  # in seconds
_DO_CREATE_DROPLET_URL = 'https://api.digitalocean.com/v2/droplets'



def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    run = (
        jdata['failcount'] >= redata['trigger'] and
        (time.time() - float(redata['lastrun'])) >= redata['frequency'] and
        redata['data']['call_on'] in jdata['check']['status']
    )
    if run:
        api_key = redata['data']['api_key']
        data = {
            'name': '%s-%s' % (redata['data']['name_prefix'],
                               time.strftime('%Y%m%d%H%M%S')),
            'region': redata['data']['region'],
            'size': redata['data']['size'],
            'image': redata['data']['image'],
            'ssh_keys': [key.strip()
                         for key in redata['data']['ssh_keys'].splitlines()
                         if key.strip()],
            'backups': bool(redata['data']['backups']) or False,
            'ipv6': bool(redata['data']['ipv6']) or False,
            'private_networking': (bool(redata['data']['private_networking']) or
                                   False),
        }
        return CallDO(api_key, data)


def CallDO(api_key, data):
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
    }
    payload = json.dumps(data)
    r = requests.post(_DO_CREATE_DROPLET_URL, timeout=_HTTP_TIMEOUT,
                      data=payload, headers=headers, verify=True)
    assert r.status_code >= 200 and r.status_code < 400, \
        'Invalid HTTP status code received: %d - %s.' % (r.status_code, r.text)
    return True


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning("digitalocean-new-droplet: Reaction {id} failed: {message}".format(
            id=redata['id'], message=e.message))
        return False
