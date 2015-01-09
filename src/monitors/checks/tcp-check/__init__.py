#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: tcp-check module
# ------------------------------------------------------------------
# This is a moduel for performing tcp based health checks.
# This will return true if no errors or false if there are errors
# ------------------------------------------------------------------
# Version: Alpha.20140618
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
######################################################################

import socket


def check(**kwargs):
    """ Perform a tcp connection to the specified IP and PORT """
    jdata = kwargs['jdata']

    # Build socket Connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Sets realistic timeout value
    s.settimeout(5)
    try:
        result = s.connect_ex((jdata['data']['ip'], int(jdata['data']['port'])))
    except socket.error:
        return False

    if result != 0:
        return False
    else:
        return True
