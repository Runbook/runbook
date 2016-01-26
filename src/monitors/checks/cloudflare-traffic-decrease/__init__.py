import time
import requests
import cloudflare


def check(**kwargs):
    ''' Grab Zone Analytics from CloudFlare API and determine status '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    # Grab and process metrics
    metrics = cloudflare.get_zone_analytics(jdata['data']['email'],
                                            jdata['data']['apikey'],
                                            jdata['data']['domain'],
                                            logger,
                                            jdata['data']['start_time'],
                                            "0")
    if not metrics:
        return None
    time_pattern = "%Y-%m-%dT%H:%M:%SZ"
    time_delta = metrics['query']['time_delta'] * 60

    previous_interval = metrics['result']['timeseries'][-2]
    current_interval = metrics['result']['timeseries'][-1]

    # Calculate whether traffic increased or not
    percent = ((float(current_interval['requests']['all']) + 1) /
               (float(previous_interval['requests']['all']) + 1)) * 100

    msg = "cloudflare-traffic-decrease:"
    msg = msg + " current_requests=%s" % str(current_interval['requests']['all'])
    msg = msg + " previous_requests=%s" % str(previous_interval['requests']['all'])
    msg = msg + " percent=%s" % str(percent)
    logger.debug(msg)

    if percent > 100:
        if "true" in jdata['data']['return_value']:
            return False
        else:
            return True
    delta = 100 - percent
    if delta > float(jdata['data']['threshold']):
        if "true" in jdata['data']['return_value']:
            return True
        else:
            return False
    else:
        if "true" in jdata['data']['return_value']:
            return False
        else:
            return True
