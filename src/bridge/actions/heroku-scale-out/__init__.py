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

    # Check if reaction should run on fails or true
    if redata['data']['call_on'] == 'true':
        run = False

    # If all checks out run it, or say i skipped
    if run:
        return action(redata, jdata)
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

    # Check if reaction should run on fails or true
    if redata['data']['call_on'] == 'false':
        run = False

    # If all checks out run it, or say i skipped
    if run:
        return action(redata, jdata)
    else:
        return None



def action(redata, jdata):
    ''' Perform Heroku Actions '''
    # Ready API Request Data
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
    url = "https://api.heroku.com/apps/" + redata['data']['appname'] + "/formation"

    # Perform API Call to get list of formations
    try:
        result = requests.get(url, timeout=timeout, headers=headers, verify=True)
    except:
        # If fail return False to mark reaction false
        return False
        line = "heroku-scale-out: Could not connect to Heroku for reaction %s" % redata['id']
        syslog.syslog(syslog.LOG_INFO, line)
    # Log heroku results for troubleshooting later
    line = "heroku-scale-out: Got status code reply %d from Heroku for reaction %s" % (result.status_code, redata['id'])
    syslog.syslog(syslog.LOG_DEBUG, line)

    # if we get a good return
    if result.status_code == 200:
        retdata = json.loads(result.text)    
        current_size = None
        current_quantity = None
        for formation in retdata:
            if formation['type'] == redata['data']['dyno_type']:
                current_quantity = int(formation['quantity'])
                # Set current size to a number value for comparison on scale ups
                if formation['size'] == "1X":
                    current_size = 1
                elif formation['size'] == "2X":
                    current_size = 2
                else:
                    current_size = 3

        run = False
        # If the current quantity is less than max_quantity let's scale it!
        if current_quantity < int(redata['data']['max_quantity']):
            new_quantity = current_quantity + 1
            run = True

        if run == True:
            # Create new payload for scaling and url
            payload = { 'quantity' : new_quantity }
            json_payload = json.dumps(payload)
            url = url + "/" + redata['data']['dyno_type']
            # make request to scale
            try:
                result = requests.patch(url, timeout=timeout, headers=headers, data=json_payload, verify=True)
            except:
                # errors
                return False
                line = "heroku-scale-out: Could not connect to Heroku for reaction %s" % redata['id']
                syslog.syslog(syslog.LOG_INFO, line)
            # Process results
            # Log heroku results for troubleshooting later
            line = "heroku-scale-out: Got status code reply %d from Heroku for reaction %s" % (result.status_code, redata['id'])
            syslog.syslog(syslog.LOG_DEBUG, line)
            # Verify we got a 200 and set as success, or set as failure
            if result.status_code == 200:
                return True
            else:
                line = "heroku-scale-out: Reaction %s got %s from Heroku after making a request to %s" % (redata['id'], result.text, url)
                syslog.syslog(syslog.LOG_DEBUG, line)
                return False
        else:
            line = "heroku-scale-out: Reaction %s is already scaled to the max quantity" % (redata['id'])
            syslog.syslog(syslog.LOG_DEBUG, line)
            return None
    else:
        line = "heroku-scale-out: Reaction %s got %s from Heroku after making a request to %s" % (redata['id'], result.text, url)
        syslog.syslog(syslog.LOG_DEBUG, line)
        return False
