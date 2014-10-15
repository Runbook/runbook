#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: Ping
# ------------------------------------------------------------------
# This is a module for performing ICMP ping health checks.
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Version: Alpha.20140618
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
######################################################################

import subprocess
import os
import re


def check(data):
    """ Perform a icmp ping to the specified IP or hostname """
    run = True
    # Search for bad stuff
    pattern = [".*255$"]
    for regex in pattern:
        match = re.search(regex, data['data']['host'])
        if match:
            run = False

    if run is False:
        return False
    else:
        DEVNULL = open(os.devnull, 'wb')
        # ping -c 1 check, -W 3 second timeout, -q quietish
        cmd = ['/bin/ping', '-c', '1', '-W', '3', '-q', data['data']['host']]
        result = subprocess.call(
            cmd, shell=False, stdout=DEVNULL, stderr=subprocess.STDOUT)
        DEVNULL.close()
        if result != 0:
            return False
        else:
            return True
