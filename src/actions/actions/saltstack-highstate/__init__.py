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
        return callSalt(redata, jdata, logger)
    else:
        return None

def callSalt(redata, jdata, logger):
    ''' Perform actual call '''
    url = redata['data']['url']
    payload = redata['data']
    try:
        req = requests.post(url, data=payload, timeout=3.00, verify=False)
    except:
        return False
    if req.status_code == 200:
        line = "saltstack-highstate: Reqeust to %s sent for monitor %s - Successful" % (url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = "saltstack-highstate: Request to %s sent for monitor %s - False" % (url, jdata['cid'])
        logger.info(line)
        return False
