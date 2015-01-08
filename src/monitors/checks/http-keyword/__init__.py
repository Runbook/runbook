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


def check(data):
    """ Perform a http get request and validate the return code """
    headers = {'host': data['data']['host']}
    timeout = 3.00
    url = data['data']['url']
    try:
        result = requests.get(
            url, timeout=timeout, headers=headers, verify=False, stream=True)

        stream = cStringIO.StringIO()
        length = 0
        for chunk in result.iter_content(2048, decode_unicode=True):
            stream.write(chunk)
            length += len(chunk)
            if length > get_max_size():
                break
        
        retext = stream.getvalue()
        stream.close()
        result.close()
    except:
        return False
    if data['data']['regex'] == "True":
        match = re.search(data['data']['keyword'], retext)
        if match:
            if data['data']['present'] == "True":
                return True
            else:
                return False
        else:
            if data['data']['present'] == "False":
                return True
            else:
                return False
    else:
        if data['data']['keyword'] in retext:
            if data['data']['present'] == "True":
                return True
            else:
                return False
        else:
            if data['data']['present'] == "False":
                return True
            else:
                return False
