#!/usr/bin/python
######################################################################
# Cloud Routes Actioner
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import requests
import json
import time


def false(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has false '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'true':
        run = False

    if run:
        return call(redata, jdata)
    else:
        return None


def true(redata, jdata, rdb, r_server):
    ''' This method will be called when a monitor has passed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'false':
        run = False

    if run:
        return call(redata, jdata)
    else:
        return None


def call(redata, jdata):
    ''' Perform actual call '''
    url = "https://api.commando.io/v1/recipes/%s/execute" % redata['data']['recipe_id']
    payload = {
        'server' : redata['data']['server_id'],
        'halt_on_stderr' : redata['data']['halt_on_stderr'],
        'notes' : 'Execution called by runbook.io'
    }
    try:
        req = requests.post(url, data=payload, auth=(redata['data']['user'], redata['data']['apikey']), timeout=3.0, verify=False)
    except:
        return False
    if req.status_code == 202:
        line = "commando-single: Reqeust to %s sent for monitor %s - Successful - %d" % (url, jdata['cid'], req.status_code)
        syslog.syslog(syslog.LOG_INFO, line)
        return True
    else:
        line = "commando-single: Request to %s sent for monitor %s - False - %d" % (url, jdata['cid'], req.status_code)
        syslog.syslog(syslog.LOG_INFO, line)
        line = "commando-single: Debug Reply: %s" % req.text
        syslog.syslog(syslog.LOG_DEBUG, line)
        return False
