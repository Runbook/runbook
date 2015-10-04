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
    last_time = int(time.mktime(time.strptime(metrics['query']['until'], time_pattern)))
    time_delta = metrics['query']['time_delta'] * 60
    previous_end_time = last_time - time_delta

    previous_interval = {}
    current_interval = {}

    # Grab previous interval from metrics
    for stats in metrics['result']['timeseries']:
        stats_end_time = int(time.mktime(time.strptime(stats['until'], time_pattern)))
        if stats_end_time == previous_end_time:
            previous_interval = stats
        elif stats_end_time == last_time:
            current_interval = stats

    # Calculate whether traffic increased or not
    percent = ((float(current_interval['requests']['all']) + 1) /
               (float(previous_interval['requests']['all']) + 1)) * 100.00
    percent = percent - 100
    msg = "cloudflare-traffic-increase:"
    msg = msg + " current_requests=%s" % str(current_interval['requests']['all'])
    msg = msg + " previous_requests=%s" % str(previous_interval['requests']['all'])
    msg = msg + " percent=%s" % str(percent)
    logger.debug(msg)
    if percent > float(jdata['data']['threshold']):
        if "true" in jdata['data']['return_value']:
            return True
        else:
            return False
    else:
        if "true" in jdata['data']['return_value']:
            return False
        else:
            return True
