######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Base Monitor Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectMultipleField
from wtforms.validators import DataRequired


class BaseCheckForm(Form):

    def __init__(self, *args, **kwargs):                                        
        super(BaseCheckForm,self).__init__(*args, **kwargs)                          

    ''' Class that creates an TCP Check form for the dashboard '''
    name = TextField(
        "Name",
        validators=[DataRequired(message='Name is a required field')],
        description="""
            A user defined name for the Runbook Monitor. Name can be alphanumeric and contain special characters.
        """,
    )
    reactions = SelectMultipleField(
        "Reactions",
        description="""
            Select the reaction or reactions you would like to execute with this monitor
        """,
    )

    # Common placeholder values
    placeholders = {
        'name' : 'Name',
        'email' : 'user@example.com',
        'domain' : 'example.com',
        'apikey' : 'API Key',
        'token' : '123abc456efg',
        'threshold' : '10',
        'hostname' : 'example.com',
        'host' : 'example.com',
        'url' : 'https://example.com/server-health',
        'extra_headers' : 'header:value',
        'port' : '443',
        'ip' : '10.0.0.1',
    }

    # Common description values
    descriptions = {
        'cloudflare' : {
            'email' : "The email address used to identify your CloudFlare account",
            'timespan' : "Select the time span to use for CloudFlare's traffic analytics. For example if you wish to compare the last 1 hour with the previous simply select 1 hour. Any time span less than 1 hour will require a CloudFlare Pro account or better",
        },
        'digitalocean' : {
            'dropletid' : "Specify the ID number of the Droplet you wish to monitor. This ID can be obtained from the DigitalOcean administrative dashboard."
        },
        'heroku' : {
            'appname' : "Specify the Heroku application name to monitor",
            'dynoname' : "Specify the name of the Dyno/s you wish to monitor (i.e. Web, Worker)"
        },
        'linode' : {
            'linodeid' : "Specify the ID number of the Node Server you wish to monitor. This ID can be obtained from the Linode administrative dashboard."
        },
        'email' : "Specify an email address to be used for this monitor",
        'domain' : "Specify a the domain to be used with this monitor",
        'apikey' : "API Key used to access the service API",
        'url' : "Enter a URL such as https://10.0.0.1/login",
        'host' : "The host header allows you to specify which domain the request will be made for. This is useful for addressing a domain that is different than that of the URL",
        'http_codes' : "Select one or more HTTP Status Code that this monitor should expect as a result",
        'extra_headers' : "Additional HTTP Headers. Headers can be specified as name:value, listed one per line",
        'status' : "Select one or more Status that this monitor should expect as a result",
        'return_value' : "Specify whether this monitor is returned as True or False when defined conditions are found",
        'hostorip' : "Specify a Host or IP for this monitor",
        'token' : "Specify the access token for the service API",
        'port' : "Specify the Port to use for this monitor",
    }

    webhook_include = "monitors/webhooks/general.html"


if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
