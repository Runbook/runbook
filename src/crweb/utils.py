######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Utilities / Common / Helper Functions
######################################################################

# Common Functions
# ------------------------------------------------------------------

import cookies
from web import app


def verifyLogin(secretkey, mxtime, cookdata):
    ''' This verifies the cookie being sent from the browser '''
    string = cookdata.get('loggedin')
    uid = cookies.verifyCdata(string, secretkey, mxtime)
    return uid


def startData(user=None):
    ''' This will set some common parameters for the data dictionary '''
    data = {}
    if user:
        data['status'] = user.status
        data['company'] = user.company
        data['loggedin'] = True
        if user.acttype == "lite" or user.acttype == "free":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes')]
            data['limit'] = 10
            data['rlimit'] = 50
            data['dataret'] = 86400
            data['acttype'] = "Lite"
            data['cost'] = "Free"
        elif user.acttype == "lite-v2":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes')]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            data['dataret'] = 86400
            data['acttype'] = "Lite"
            data['cost'] = "Free"
        elif user.acttype == "enterprise":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes'),
                ('2mincheck', 'Every 2 Minutes'),
                ('30seccheck', 'Every 30 Seconds')
            ]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            data['cost'] = float(user.subplans) * 6.00
            data['dataret'] = 16070400
            data['acttype'] = "Enterprise"
        else:
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes'),
                ('2mincheck', 'Every 2 Minutes'),
                ('30seccheck', 'Every 30 Seconds')
            ]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            if "yearly" in user.subscription:
                permon = .75 * 12.00
            else:
                permon = 1.00
            data['cost'] = float(user.subplans) * permon
            data['dataret'] = 604800
            data['acttype'] = "Pro"
    data['js_bottom'] = []
    data['js_header'] = []
    data['stripe_pubkey'] = app.config['STRIPE_PUBKEY']
    data['subplans'] = user.subplans
    data['subscription'] = user.subscription
    return data
