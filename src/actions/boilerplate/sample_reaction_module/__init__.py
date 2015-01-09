# save this file/folder to /src/actions/actions/some-reaction


#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

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
        return actionName(redata, jdata, logger)
    else:
        return None


def actionName(redata, jdata, logger):
    ''' Perform Some Action(s) '''
    try:
        react = reaction.action(
            redata=kwargs['redata'],
            jdata=kwargs['jdata'],
            rdb=kwargs['rdb'],
            r_server=kwargs['r_server'],
            config=kwargs['config'])
    except Exception as e:
        logger.error("Got error when attempting to run reaction {0} \
            for monitor {1}".format(redata['rtype'], jdata['cid']))
