#!/usr/bin/python
"""Monitors SSL certificate for correct CN.

Note: works only on TLSv1 and higher.
"""

import ssl
import OpenSSL


def _check(jdata, logger):
    """Checks server SSL certificate for correct CN."""
    host = jdata['data']['host']
    port = int(jdata['data'].get('port', 443))
    expected_hostname = jdata['data']['expected_hostname']
    cert = ssl.get_server_certificate((host, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    actual_hostname = x509.get_subject().CN
    logger.debug('Hostname in certificate: %s' % actual_hostname)
    assert actual_hostname == expected_hostname, "Hostname doesn't match."
    return True


def check(**kwargs):
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    try:
        return _check(jdata)
    except Exception, e:
        logger.warning(e.message)
        return False
