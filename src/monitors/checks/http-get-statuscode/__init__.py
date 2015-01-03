#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: http-get-statuscode module
# ------------------------------------------------------------------
# This is a moduel for performing http get based health checks.
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Version: Alpha.20140618
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
######################################################################

import requests


def check(**kwargs):
    """ Perform a http get request and validate the return code """
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    headers = {'host': jdata['data']['host']}
    timeout = 3.00
    url = jdata['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False)
    except Exception as e:
        line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
               'had an exception: {2}'.format(url, jdata['cid'], e)
        logger.error(line)
        return False
    rcode = str(result.status_code)
    if rcode in jdata['data']['codes']:
        line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
               'Successful'.format(url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
               'Failure'.format(url, jdata['cid'])
        logger.info(line)
        return False
