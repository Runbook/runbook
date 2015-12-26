######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Base Reaction Form
######################################################################

from wtforms import Form
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class BaseReactForm(Form):

    ''' Class that creates a Base Reaction form for import '''
    name = TextField(
        "Name",
        description="""
            A user defined name for the Reaction. A Name can be alphanumeric and contain special characters.
        """,
        validators=[DataRequired(message='Name is a required field')])
    trigger = IntegerField(
                          "Trigger",
                          description="""
                            The Trigger value defines the number of times a monitor must return the desired state before triggering a reaction execution. If you wish to execute this reaction on the first instance of a failure set this value to 0. A value of 1 will trigger on the second instance of failure.
                          """,
                          validators=[NumberRange(
        min=0, max=999, message='Trigger must be a number between 0 - 999')])
    frequency = IntegerField(
        "Frequency",
        description="""
          The Frequency field defines the length of time (in seconds) to wait before executing the reaction again. For example if a reaction is rebooting a server that takes 1 minute to reboot it would be wise to wait at least 120 seconds before triggering another reaction execution.
        """,
        validators=[
            NumberRange(
                min=0,
                max=999999999,
                message='Frequency must be a number between 0 - 999999999')
        ]
    )

    # Common placeholder values
    placeholders = {
        'name' : 'Name',
        'email' : 'user@example.com',
        'domain' : 'example.com',
        'apikey' : 'API Key',
        'threshold' : '10',
        'hostname' : 'example.com',
        'host' : 'example.com',
        'url' : 'https://example.com/server-health',
        'extra_headers' : 'header:value',
        'port' : '443',
        'trigger' : '0',
        'frequency' : '120',
        'host_string' : 'example.com:22',
        'gateway' : 'example.com:22',
        'username' : 'root',
        'password' : 'password',
        'sshkey' : 'SSH Private Key',
        'cmd' : 'service httpd restart',
    }

    # Common description values
    descriptions = {
        'cloudflare' : {
            'email' : "The email address used to identify your CloudFlare account",
            'domain' : "Specify your CloudFlare protected domain",
            'timespan' : "Select the time span to use for CloudFlare's traffic analytics. For example if you wish to compare the last 1 hour with the previous simply select 1 hour. Any time span less than 1 hour will require a CloudFlare Pro account or better",
            'recName' : "Specify a DNS Record name, if no record name is specified the action will be performed on all records that match the defined Record Content",
            'recType' : "Specify the desired DNS Record type",
            'content' : "Specify either the IP or CNAME content",
            'ttl' : "Specify the desired DNS record TTL, in general this should be set to 1",
            'proxied' : "Specify whether this record should be proxied by CloudFlare or not. Protected records should be proxied",
        },
        'commando' : {
            'recipeID' : "Specify the ID Number of the recipe to be called. This can be obtained via Commando.io's dashboard.",
            'groupID' : "Specify the ID Number of the server group to execute against. This can be obtained via Commando.io's dashboard.",
            'serverID' : "Specify the ID Number of the server to execute against. This can be obtained via Commando.io's dashboard.",
            'haltonerror' : "Define whether the execution of this recipe should be halted if a single server experiences an error.",
            'userID' : "Specify your Commando.io User ID",
        },
        'digitalocean' : {
            'dropletid' : "Specify the ID number of the Droplet you wish to act against. This ID can be obtained from the DigitalOcean administrative dashboard.",
            'nameprefix' : "This reaction uses the name prefix and a timestamp to name the droplet. The format will be Prefix-20150102152203.",
            'region' : "Specify the DigitalOcean datacenter to perform this action against. Common values: nyc3, sfo1, ams2, lon1.",
            'size' : "Define the desired size of the Droplet. Common values: 512mb, 1gb, 2gb, 4gb.",
            'image' : "Specify the desired Droplet image to use. Common values: fedora-20-x64, ubuntu-14-04-x64.",
            'sshkeys' : "Specify an SSH key or keys to apply when provisioning. Specify keys one per line.",
            'backups' : "Define whether backups should be created for this Droplet.",
            'ipv6' : "Specify whether this Droplet should have IPV6 networking or not.",
            'privatenetworking' : "Define whether this Droplet should have a private networking interface or not.",
        },
        'heroku' : {
            'appname' : "Specify the Heroku application name to action",
            'dynoname' : "Specify the name of the Dyno/s you wish to perform an action against (i.e. Web, Worker)",
            'cmd' : "Specify the command to execute",
            'attach' : "Specify whether to stream output or not",
            'size' : "Select a desired Dyno Size",
            'dynotype' : "Define the type of Dyno this reaction affects, this is generally the process name I.E. web, worker",
        },
        'aws' : {
            'region' : "Specify the AWS region this resources resides within",
            'accessKey' : "Specify your AWS Access Key",
            'accessSecretKey' : "Specify your AWS Secret Access Key",
            'instanceID' : "Specify the ID of the instance this reaction should execute against.",
        },
        'ssh' : {
            'gateway' : "If specified the reaction will use the gateway server as a jump host",
            'host_string' : "Target host information in the format of hostname:port",
            'password' : "Password to use for password based authentication",
            'sshkey' : "SSH Private key to use for key based authentication",
            'cmd' : "Command you wish to execute on the target server",
            'username' : "Username to use during login",
        },
        'callon' : "Define whether this reaction should execute on True or False monitors",
        'email' : "Specify an email address to be used for this reaction",
        'domain' : "Specify a the domain to be used with this reaction",
        'apikey' : "API Key used to access the service API",
        'url' : "Enter a URL such as https://10.0.0.1/login",
        'host' : "The host header allows you to specify which domain the request will be made for. This is useful for addressing a domain that is different than that of the URL",
        'http_codes' : "Select one or more HTTP Status Code that this reaction should expect as a result",
        'extra_headers' : "Additional HTTP Headers. Headers can be specified as name:value, listed one per line",
        'return_value' : "Specify whether this reaction is returned as True or False when defined conditions are found",
        'username' : "Specify a username to provide to the service",
        'rackspace' : {
            'serverID' : "Specify the ID of the server in question",
            'region' : "Specify the Rackspace Datacenter region this server resides in",
            'resourceType' : "Select the type of Server this reaction is for",
        },
        'linode' : {
            'linodeID' : "Specify the ID of the Node Server",
        },
        'http' : {
            'url' : "Enter a URL such as https://10.0.0.1/login",
            'host' : "The host header allows you to specify which domain the request will be made for. This is useful for addressing a domain that is different than that of the URL",
            'http_codes' : "Select one or more HTTP Status Code that this reaction should expect as a result",
            'http_method' : "Select the desired HTTP Method to use for this request",
            'extra_headers' : "Additional HTTP Headers. Headers can be specified as name:value, listed one per line",
            'payload' : "Define a payload to send with POST and PUT methods",
        },
        'saltstack' : {
            'secretkey' : "Provide a secret key to send for API authentication",
            'tgt' : "This is a standard SaltStack targeting method, use this as you would use SaltStack from CLI",
            'matcher' : "Select the Type of Targeting method being used",
        },
    }

if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
