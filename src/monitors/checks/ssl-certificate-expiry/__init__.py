#!/usr/bin/python
"""Monitors SSL certificate validity.

Note: works only on TLSv1 and higher.
"""

import datetime
import ssl
import syslog
import OpenSSL


def _check(data):
    """Checks server SSL certificate for expiry."""
    hostname = data['data']['hostname']
    port = int(data['data'].get('port', 443))
    num_days = int(data['data'].get('num_days', 7))
    cert = ssl.get_server_certificate((hostname, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry_date = x509.get_notAfter()
    assert expiry_date, "Cert doesn't have an expiry date."
    expiry = datetime.datetime.strptime(expiry_date[:8], '%Y%m%d')
    now = datetime.datetime.now()
    days_left = (expiry - now).days
    syslog.syslog(syslog.LOG_DEBUG, 'Days left in cert expiry: %d' % days_left)
    return days_left > num_days
  

def check(data):
    try:
        return _check(data)
    except Exception, e:
        syslog.syslog(syslog.LOG_WARNING, e.message)
        return False

