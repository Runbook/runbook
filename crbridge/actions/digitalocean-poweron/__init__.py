#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import requests
import json
import time


def failed(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has failed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'healthy':
        run = False

    if run:
        return callDO(redata, jdata)
    else:
        return None


def healthy(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'failed':
        run = False

    if run:
        return callDO(redata, jdata)
    else:
        return None


def callDO(redata, jdata):
    ''' Perform actual call '''
    headers = {'Authorization': 'Bearer ' + redata['data']['apikey'],
               'Content-Type': 'application/json'}
    url = "https://api.digitalocean.com/v2/droplets/%s/actions" % str(
        redata['data']['dropletid'])
    msg = {"type": "power_on"}
    payload = json.dumps(msg)
    try:
        req = requests.post(
            url, timeout=3.0, data=payload, headers=headers, verify=True)
    except:
        return False
    if req.status_code >= 200 and req.status_code < 300:
        line = "digitalocean-poweron: Reqeust to %s sent for monitor %s - Successful" % (
            url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return True
    else:
        line = "digitalocean-poweron: Request to %s sent for monitor %s - Failed" % (
            url, jdata['cid'])
        syslog.syslog(syslog.LOG_INFO, line)
        return False
