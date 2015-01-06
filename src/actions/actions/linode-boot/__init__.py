#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import requests
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
        "LinodeID": int(redata['data']['linode_id']),
        "api_key": str(redata['data']['api_key'])
    }
    try:
        req = requests.post(
            url, timeout=3.0, data=params, verify=True)
    except:
        return False
    if req.status_code >= 200 and req.status_code < 300:
        if len(req.json['ERRORARRAY']) > 0:
            try:
                error_message = str(req.json()['ERRORARRAY'][0]['ERRORMESSAGE'])
            except:
                error_message = "Unknown Error"
            line = 'linode-reboot: Request to {0} sent for monitor {1} - \
                False - {3}'.format(url, jdata['cid'], error_message)
            logger.info(line)
            return False
        else:
            line = 'linode-reboot: Request to {0} sent for monitor {1} - \
                Successful'.format(url, jdata['cid'])
            logger.info(line)
        return True
