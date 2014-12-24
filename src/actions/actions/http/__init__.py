"""HTTP - GET / POST reaction"""

import requests
import syslog
from ..utils import ParseHeaders, ShouldRun

_HTTP_REQUEST_TIMEOUT = 10.0  # in seconds


def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    if ShouldRun(redata, jdata):
        http_verb = redata['data']['http_verb'] or 'GET'
        url = redata['data']['url']
        assert url, 'URL is required.'
        extra_headers = ParseHeaders(redata['data']['extra_headers'] or '')
        if http_verb == 'GET':
            status = http_get(url, extra_headers)
        elif http_verb == 'POST':
            payload = redata['data']['payload'] or ''
            status = http_post(url, extra_headers, payload)
        else:
            return  # Notify that we skipped the reaction
        assert status >= 200 and status < 400, \
            'Invalid HTTP Status code received: %d' % status
        return True


def http_get(url, extra_headers):
    r = requests.get(url, timeout=_HTTP_REQUEST_TIMEOUT, headers=extra_headers,
                     verify=False)
    return r.status_code


def http_post(url, extra_headers, payload):
    r = requests.post(url, timeout=_HTTP_REQUEST_TIMEOUT, headers=extra_headers,
                      data=payload, verify=False)
    return r.status_code


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:
        redata = kwargs['redata']
        syslog.syslog(
            syslog.LOG_WARNING,
            'http: Reaction {id} failed: {message}'.format(
                id=redata['id'], message=e.message))
        return False
