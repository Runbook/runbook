# Update CloudFlare DNS record

# Action Helpers
import cloudflare
import json
import time


def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return run_reaction(redata, jdata, logger)
    else:
        return None


def run_reaction(redata, jdata, logger):
    ''' This method performs the heavy lifting '''
    setting = "security_level"
    value = {'value' : redata['data']['action']}
    return cloudflare.change_zone_settings(redata['data']['email'],
                                           redata['data']['apikey'],
                                           redata['data']['domain'],
                                           logger,
                                           setting,
                                           value)
