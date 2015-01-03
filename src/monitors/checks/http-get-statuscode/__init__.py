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
    headers = {'host': jdata['data']['host']}
    timeout = 3.00
    url = jdata['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False)
    except:
        return False
    rcode = str(result.status_code)
    if rcode in jdata['data']['codes']:
        return True
    else:
        return False
