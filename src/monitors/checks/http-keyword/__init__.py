#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: http-keyword module
# ------------------------------------------------------------------
# This is a module for performing http keyword searches.
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Version: Alpha.20140827
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
######################################################################

import requests
import re
import cStringIO

# currently the http get size limit is 2MB
# change the following function to allow for per user, size limit
def get_max_size():
    return 2*1024*1024

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
            url, timeout=timeout, headers=headers, allow_redirects=True, verify=False, stream=True)
    except Exception as e:
        line = 'http-keyword: Reqeust to {0} sent for monitor {1} - ' \
               'had an exception: {2}'.format(url, jdata['cid'], e)
        logger.debug(line)
        return False
        
    stream = cStringIO.StringIO()
    length = 0
    for chunk in result.iter_content(8192, decode_unicode=False):
        stream.write(chunk)
        length += len(chunk)
        if length > get_max_size():
            break
        
    retext = stream.getvalue()
    stream.close()
    result.close()
    retext = retext.decode('utf8')
    if jdata['data']['regex'] == "True":
        match = re.search(jdata['data']['keyword'], retext)
        if match:
            if jdata['data']['present'] == "True":
                return True
            else:
                return False
        else:
            if jdata['data']['present'] == "False":
                return True
            else:
                return False
    else:
        if jdata['data']['keyword'] in retext:
            if jdata['data']['present'] == "True":
                return True
            else:
                return False
        else:
            if jdata['data']['present'] == "False":
                return True
            else:
                return False
