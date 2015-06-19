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

# TODO: There should be a common lib where these utility functions can be
# stored. For now, we duplicate code :-(
def ParseHeaders(headers_str):
    headers = {}
    for header in str.splitlines(str(headers_str)):
        header = header.strip()
        # Ignore empty lines
        if not header:
            continue
        key, value = header.split(':')
        key = key.strip()
        value = value.strip()
        assert key
        assert value
        headers[key] = value
    return headers



def check(**kwargs):
    """ Perform a http get request and validate the return code """
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    headers = {}
    if 'extra_headers' in jdata['data']:
      headers = ParseHeaders(jdata['data']['extra_headers'])
    headers['host'] = jdata['data']['host']
    timeout = 3.00
    url = jdata['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False, stream=True)
    except Exception as e:
        line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
               'had an exception: {2}'.format(url, jdata['cid'], e)
        logger.error(line)
        return False
    rcode = str(result.status_code)
    result.close()
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
