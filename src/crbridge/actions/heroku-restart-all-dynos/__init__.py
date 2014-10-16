#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import syslog
import time
import json
import base64
import requests

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

    # Check if reaction should run on fails or healthy
    if redata['data']['call_on'] == 'healthy':
        run = False

    # If all checks out run it, or say i skipped
    if run:
        return action(redata, jdata)
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

    # Check if reaction should run on fails or healthy
    if redata['data']['call_on'] == 'failed':
        run = False

    # If all checks out run it, or say i skipped
    if run:
        return action(redata, jdata)
    else:
        return None



def action(redata, jdata):
    ''' Perform Heroku Actions '''
    # Ready API Request
    # Generate Base64 encoded API Key
    basekey = base64.b64encode(":" + redata['data']['apikey'])
    # Create headers for API call
    headers = {
        "Accept" : "application/vnd.heroku+json; version=3",
        "Authorization" : basekey
    }
    # Set Timeout value for API Call
    timeout = 5.00
    # URL to request
    url = "https://api.heroku.com/apps/%s/dynos" % redata['data']['appname']
    # Perform API Call
    try:
        result = requests.delete(
          url,
          timeout=timeout,
          headers=headers,
          verify=True
        )
    except:
        # If fail return False to mark reaction failed
        return False
        line = ("heroku-restart-dyno: Could not connect to Heroku"
                " for monitor %s") % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)

    # Process results
    # Log heroku results for troubleshooting later
    line = ("heroku-restart-dyno: Got status code reply %d from Heroku"
            " for monitor %s") % (result.status_code, jdata['cid'])
    syslog.syslog(syslog.LOG_DEBUG, line)
    # Verify we got a 201 and set as success, or set as failure
    if result.status_code == 202:
        return True
    else:
        line = ("heroku-restart-dyno: Monitor %s got %s from Heroku after"
                " making a request to %s") % (jdata['cid'], result.text, url)
        syslog.syslog(syslog.LOG_DEBUG, line)
        return False
