#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: linode-status module
# ------------------------------------------------------------------
# This is a module for performing Linode server status checks.
# This will return true if if the Linode's current status is one
# of those expected by the monitor, false otherwise. Anything other
# than 2xx HTTP status from Linode will return false.
# ------------------------------------------------------------------
######################################################################

import requests
import json

http_timeout = 5.0
url = 'https://api.linode.com/'

def check(**kwargs):
    ''' Perform a Linode info retrieval and check status '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    params = {
        "api_action": "linode.list",
        "LinodeID": int(jdata['data']['linodeid']),
        "api_key": str(jdata['data']['apikey'])
    }
    
    try:
        req = requests.get(
            url, timeout=http_timeout, params=params, verify=True)
    except Exception as e:
        line = 'linode-status: Reqeust to {0} sent for monitor {1} - ' \
               'had an exception: {2}'.format(url, jdata['cid'], e)
        logger.error(line)
        return False

    if req.status_code < 200 or req.status_code >= 300:
        line = 'linode-status: Reqeust to {0} sent for monitor {1} - ' \
               'non-success HTTP code'.format(url, jdata['cid'])
        logger.warning(line)
        return False

    nodereply = json.loads(req.text)
    try:
      status = nodereply['DATA'][0]['STATUS']
    except:
      line = 'linode-status: Recieved invalid json response for' \
              ' monitor {0}, {1}'.format(jdata['cid'], req.text)
      logger.debug(line)
      return False
    if str(status) in jdata['data']['status']:
        line = 'linode-status: Reqeust to {0} sent for monitor {1} - ' \
               'Successful'.format(url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = 'linode-status: Reqeust to {0} sent for monitor {1} - ' \
               'Failure'.format(url, jdata['cid'])
        logger.info(line)
        return False
