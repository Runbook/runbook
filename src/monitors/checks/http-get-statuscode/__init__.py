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


def check(data):
    """ Perform a http get request and validate the return code """
    headers = {'host': data['data']['host']}
    timeout = 3.00
    url = data['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False, stream=True)
    except:
        return False
    rcode = str(result.status_code)
    result.close()
    if rcode in data['data']['codes']:
        return True
    else:
        return False
