#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import requests
import json
import time


def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return call_linode(redata, jdata, logger)
    else:
        return None


def call_linode(redata, jdata, logger):
    ''' Perform actual call '''
    url = 'https://api.linode.com/'
    params = {
        "api_action": "linode.reboot",
        "LinodeID": redata['data']['linode_id'],
        "api_key": redata['data']['api_key']
    }
    payload = json.dumps(params)
    try:
        req = requests.post(
            url, timeout=3.0, data=payload, verify=True)
    except:
        return False
    if req.status_code >= 200 and req.status_code < 300:
        line = 'linode-reboot: Requset to {0} sent for monitor {1} - \
                Successful'.format(url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = 'digitalocean-reboot: Request to {0} sent for monitor {1} - \
                False'.format(url, jdata['cid'])
        logger.info(line)
        return False
