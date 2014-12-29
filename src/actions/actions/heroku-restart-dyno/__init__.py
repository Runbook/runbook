#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import time
import json
import base64
import requests


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
        return callAction(redata, jdata, logger)
    else:
        return None


def callAction(redata, jdata, logger):
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
    url = "https://api.heroku.com/apps/%s/dynos/%s" % (
      redata['data']['appname'],
      redata['data']['dynoname']
    )
    # Perform API Call
    try:
        result = requests.delete(
          url,
          timeout=timeout,
          headers=headers,
          verify=True
        )
    except:
        # If fail return False to mark reaction false
        return False
        line = ("heroku-restart-dyno: Could not connect to Heroku"
                " for monitor %s") % jdata['cid']
        logger.info(line)

    # Process results
    # Log heroku results for troubleshooting later
    line = ("heroku-restart-dyno: Got status code reply %d from Heroku"
            " for monitor %s") % (result.status_code, jdata['cid'])
    logger.debug(line)
    # Verify we got a 201 and set as success, or set as failure
    if result.status_code == 202:
        return True
    else:
        line = ("heroku-restart-dyno: Monitor %s got %s from Heroku after"
                " making a request to %s") % (jdata['cid'], result.text, url)
        logger.debug(line)
        return False
