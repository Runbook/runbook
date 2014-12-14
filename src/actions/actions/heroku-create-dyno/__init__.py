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

def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
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
        return callAction(redata, jdata)
    else:
        return None


def callAction(redata, jdata):
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
    url = "https://api.heroku.com/apps/" + redata['data']['appname'] + "/dynos"
    # Setting payload of user input from /dashboard/reactions/heroku-create-dyno
    payload = {
        'command' : redata['data']['cmd'],
        'size' : redata['data']['size']
    }
    # Heroku accepts boolean but db is string
    if redata['data']['attach'] == "true":
        payload['attach'] = True
    else:
        payload['attach'] = False
    # Convert payload to json
    json_payload = json.dumps(payload)

    # Perform API Call
    try:
        result = requests.post(url, timeout=timeout, headers=headers, data=json_payload, verify=True)
    except:
        # If fail return False to mark reaction false
        return False
        line = "heroku-create-dyno: Could not connect to Heroku for monitor %s" % jdata['cid']
        syslog.syslog(syslog.LOG_INFO, line)

    # Process results
    # Log heroku results for troubleshooting later
    line = "heroku-create-dyno: Got status code reply %d from Heroku for monitor %s" % (result.status_code, jdata['cid'])
    syslog.syslog(syslog.LOG_DEBUG, line)
    # Verify we got a 201 and set as success, or set as failure
    if result.status_code == 201:
        return True
    else:
        line = "heroku-create-dyno: Monitor %s got %s form Heroku after making a request to %s" % (jdata['cid'], result.text, url)
        syslog.syslog(syslog.LOG_DEBUG, line)
        return False
