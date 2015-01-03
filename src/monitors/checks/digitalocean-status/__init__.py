#!/usr/bin/python
######################################################################
# Cloud Routes Availability Manager: digitalocean-status module
# ------------------------------------------------------------------
# This is a moduel for performing DigitalOcean droplet status checks.
# This will return true if if the droplet's current status is one
# of those expected by the monitor, false otherwise. Anything other
# than 2xx HTTP status from DigitalOcean will return false.
# ------------------------------------------------------------------
######################################################################

import requests


http_timeout = 5.0
do_droplet_info_url = 'https://api.digitalocean.com/v2/droplets/{0}'


def check(**kwargs):
    ''' Perform a DigitalOcean droplet info retrieval and check status '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(jdata['data']['apikey'])}
    url = do_droplet_info_url.format(jdata['data']['dropletid'])

    try:
        req = requests.get(
            url, timeout=http_timeout, headers=headers, verify=True)
    except Exception as e:
        line = 'digitalocean-status: Reqeust to {0} sent for monitor {1} - ' \
               'had an exception: {2}'.format(url, jdata['cid'], e)
        logger.error(line)
        return False

    if req.status_code < 200 or req.status_code >= 300:
        line = 'digitalocean-status: Reqeust to {0} sent for monitor {1} - ' \
               'non-success HTTP code'.format(url, jdata['cid'])
        logger.warning(line)
        return False

    status = req.json()['droplet']['status']
    if status in jdata['data']['status']:
        line = 'digitalocean-status: Reqeust to {0} sent for monitor {1} - ' \
               'Successful'.format(url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = 'digitalocean-status: Reqeust to {0} sent for monitor {1} - ' \
               'Failure'.format(url, jdata['cid'])
        logger.info(line)
        return False
