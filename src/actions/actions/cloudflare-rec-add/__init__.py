#!/usr/bin/python
#####################################################################

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
    rec_data = {
        'name' : redata['data']['rec_name'],
        'type' : redata['data']['rec_type'],
        'content' : redata['data']['content']
    }
    zoneid = cloudflare.get_zoneid(
          redata['data']['email'],
          redata['data']['apikey'],
          redata['data']['domain'],
          logger)
    if zoneid is not None:
        check = cloudflare.get_recs(
            redata['data']['email'],
            redata['data']['apikey'],
            zoneid,
            logger,
            page=1,
            search=rec_data,
            )
        logger.debug("cloudflare-rec-add: Got Records " + json.dumps(check))
        if len(check) == 0:
            logger.debug("cloudflare-rec-add: Found " + str(len(check)) + " matching records")
            rec_data['ttl'] = redata['data']['ttl']
            if "true" in redata['data']['proxied']:
                rec_data['proxied'] = True
            else:
                rec_data['proxied'] = False
            result = cloudflare.add_rec(
                redata['data']['email'],
                redata['data']['apikey'],
                zoneid,
                logger,
                rec_data)
            if result:
                logger.info("cloudflare-rec-add: Successfully added record for monitor " + redata['id'])
                return True
            else:
                logger.debug("cloudflare-rec-add: Failed to add record for monitor " + redata['id']) 
                return False
        else:
            logger.debug("cloudflare-rec-add: Found " + str(len(check)) + " matching records")
            return None
    else:
        logger.debug("cloudflare-rec-add: Could not pull zone id for domain " + redata['data']['domain'] + " for monitor  " + redata['id'])
        return False
