######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Papertrail Webhook Monitor module
######################################################################

import json
import random

def webCheck(request, monitor, urldata, rdb):
    ''' Process the webbased api call '''
    replydata = {
        'headers': {'Content-type': 'application/json'}
    }
    rdata = {}
    bad = [
            "Uh oh, something failed...",
            "I just can't do it Captain, I just don't have the power!",
            "I'm sorry, Dave. I'm afraid I can't do that.",
    ]
    good = [
            "Got it!",
            "Sure thing boss.",
            "Alright, alright alright.",
            "Done!",
    ]
            
            

    # Ensure method is POST
    if request.method == "POST":
        request_verify = True
    else:
        request_verify = False

    # Verify and then send web check Monitor
    monitor.get(urldata['cid'], rdb)
    # Verify check_key and api_type matches monitor for cid
    if urldata['check_key'] == monitor.url and \
            urldata['atype'] == monitor.ctype and \
            monitor.data['token'] == request.values['token']:
        # Ensure action is false or true
        if "False" in request.values['text']:
            action = "false"
        else:
            action = "true"
        if action == "false" or action == "true":
            # Set new status (not saved until monitor.webCheck is performed
            monitor.healthcheck = action
            if request_verify is True:
                # Send web based health check to dcqueues
                result = monitor.webCheck(rdb)
            else:
                result = False
            if result:
                rdata['text'] = random.choice(good)
            else:
                rdata['text'] = random.choice(bad)
        else:
            rdata['text'] = random.choice(bad)
    else:
        rdata['text'] = "Sorry, invalid key."
    replydata['data'] = json.dumps(rdata)
    return replydata
