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
    r_server = kwargs['r_server']
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
        return callAction(redata, jdata, r_server, logger)
    else:
        return None


def callAction(redata, jdata, r_server, logger):
    ''' Perform Heroku Actions '''
    # Ready API Request Data
    # Generate Base64 encoded API Key
    basekey = base64.b64encode(":" + redata['data']['apikey'])
    # Redis key for saved value
    rkey = "heroku-rollback-release:" + redata['id']
    # Create headers for API call
    headers = {
        "Accept" : "application/vnd.heroku+json; version=3",
        "Authorization" : basekey
    }
    # Set Timeout value for API Call
    timeout = 5.00
    # URL to request
    baseurl = "https://api.heroku.com/apps/" + redata['data']['appname']
    url = baseurl + "/dynos"

    # Perform API Call to get list of dynos
    try:
        result = requests.get(
          url,
          timeout=timeout,
          headers=headers,
          verify=True
        )
    except:
        # If fail return False to mark reaction false
        line = ("heroku-rollback-release:"
               " Could not connect to Heroku for reaction %s") % redata['id']
        logger.info(line)
        return False
    # Log heroku results for troubleshooting later
    line = ("heroku-rollback-release: Got status code reply %d "
            "from Heroku for reaction %s") % (result.status_code, redata['id'])
    logger.debug(line)

    # if we get a good return
    if result.status_code == 200:
        retdata = json.loads(result.text)
        current_release = None
        for dtype in retdata:
            current_release = int(dtype['release']['version'])

        # Check redis for a previously rolledback version
        # Heroku creates a new release for each rollback request
        redis_release = r_server.get(rkey)
        if redis_release is not None:
            if int(redis_release) < current_release:
                # if redis release is older set the current as redis
                current_release = int(redis_release)

        run = False
        # If the current quantity is greater than min_quantity let's rollback
        if current_release > int(redata['data']['min_release']):
            new_release = current_release - 1
            run = True

        if run == True:
            # Get Release info
            url = baseurl + "/releases/" + str(new_release)
            try:
                result = requests.get(
                  url,
                  timeout=timeout,
                  headers=headers,
                  verify=True
                )
            except:
                line = ("heroku-rollback-release:"
                        " Could not get list of releases"
                        " for reaction %s") % redata['id']
                logger.debug(line)
                return False

            # Get unique id for release to rollback to
            if result.status_code >= 200 and result.status_code < 300:
                retdata = json.loads(result.text)
                if 'id' in retdata:
                    releaseid = retdata['id']
                    rollback = True
                else:
                    rollback = False
            else:
                line = ("heroku-rollback-release:"
                        " Could not get info on release"
                        " for reaction %s") % redata['id']
                logger.debug(line)
                return False

            # If we got value let's continue
            if rollback:
                # Create new payload for rollback
                payload = { 'release' : releaseid }
                json_payload = json.dumps(payload)
                url = baseurl + "/releases"
                # make request to scale
                try:
                    result = requests.post(
                      url,
                      timeout=timeout,
                      headers=headers,
                      data=json_payload,
                      verify=True
                    )
                except:
                    # errors
                    line = ("heroku-rollback-release: Could not connect to "
                            "Heroku for reaction %s") % redata['id']
                    logger.info(line)
                    return False
                # Process results
                # Log heroku results for troubleshooting later
                line = ("heroku-rollback-release: Got status code reply %d "
                       "from Heroku for reaction"
                       " %s") % (result.status_code, redata['id'])
                logger.debug(line)
                # Verify we got a 200 and set as success, or set as failure
                if result.status_code == 201:
                    # If everything is good set the rollback release
                    # into redis with an expiring key
                    r_server.setex(rkey, new_release, "14400")
                    r_server.expire(rkey, "14400")
                    return True
                else:
                    line = ("heroku-rollback-release: Reaction %s got %s "
                            "from Heroku after making a request"
                            " to %s") % (redata['id'], result.text, url)
                    logger.debug(line)
                    return False
            else:
                line = ("heroku-rollback-release:"
                        " Could not get releases info"
                        " for reaction %s") % redata['id']
                logger.debug(line)
                return False
        else:
            line = ("heroku-rollback-release: Reaction %s is already "
                    "rolled back to the min_release"
                    " %s") % (redata['id'], int(redata['data']['min_release']))
            logger.debug(line)
            return None
    else:
        line = ("heroku-rollback-release: Reaction %s got %s from "
                "Heroku after making a request to "
                "%s") % (redata['id'], result.text, url)
        logger.debug(line)
        return False
