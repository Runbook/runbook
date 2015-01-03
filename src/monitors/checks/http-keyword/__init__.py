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


def check(**kwargs):
    """ Perform a http get request and validate the return code """
    jdata = kwargs['jdata']
    headers = {'host': jdata['data']['host']}
    timeout = 3.00
    url = jdata['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False)
        retext = unicode(result.text)
    except:
        return False
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
