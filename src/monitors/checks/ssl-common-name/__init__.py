#!/usr/bin/python
"""Monitors SSL certificate for correct CN.

Note: works only on TLSv1 and higher.
"""

import ssl
import syslog
import OpenSSL


def _check(data):
    """Checks server SSL certificate for correct CN."""
    host = data['data']['host']
    port = int(data['data'].get('port', 443))
    expected_hostname = data['data']['expected_hostname']
    cert = ssl.get_server_certificate((host, port), ssl_version=ssl.PROTOCOL_TLSv1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    actual_hostname = x509.get_subject().CN
    syslog.syslog(syslog.LOG_DEBUG, 'Hostname in certificate: %s' % actual_hostname)
    assert actual_hostname == expected_hostname, "Hostname doesn't match."
    return True


def check(data):
    try:
        return _check(data)
    except Exception, e:
        syslog.syslog(syslog.LOG_WARNING, e.message)
        return False
