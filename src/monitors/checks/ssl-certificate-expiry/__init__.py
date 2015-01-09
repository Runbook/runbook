#!/usr/bin/python
"""Monitors SSL certificate validity.

Note: works only on TLSv1 and higher.
"""

import datetime
import ssl
import OpenSSL


def _check(jdata, logger):
    """Checks server SSL certificate for expiry."""
    hostname = jdata['data']['hostname']
    port = int(jdata['data'].get('port', 443))
    num_days = int(jdata['data'].get('num_days', 7))
    cert = ssl.get_server_certificate(
        (hostname, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry_date = x509.get_notAfter()
    assert expiry_date, "Cert doesn't have an expiry date."
    expiry = datetime.datetime.strptime(expiry_date[:8], '%Y%m%d')
    now = datetime.datetime.now()
    days_left = (expiry - now).days
    logger.debug('Days left in cert expiry: %d' % days_left)
    return days_left > num_days


def check(**kwargs):
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    try:
        return _check(jdata, logger)
    except Exception, e:
        logger.warning(e.message)
        return False

