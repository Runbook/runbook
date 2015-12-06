######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# CloudFlare IP Replacement - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Email, IPAddress, NumberRange

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a CloudFlare Reaction form for the dashboard '''
    title = "CloudFlare: DNS Failover"
    description = """
    <P>
    This Reaction is designed for Active-Active DNS Failover. When a Monitor returns a status that matches the "Call On" value, this Reaction will query CloudFlare's API and remove records that match the defined content. If a "Record Name" is set, the reaction will only remove the IP/CNAME from that record. If the "Record Name" is not set, all DNS records with the defined content will be removed.
    </P><P>
    As this Reaction is designed for DNS Failover, if there is only one DNS record with the defined content the DNS record will not be removed. For example, if there are 2 "www.example.com" records; one that points to 10.0.0.1 and one that points to 10.0.0.2. This reaction will remove the defined record (10.0.0.1). If there was only 1 "mail.example.com" that points to 10.0.0.1, this reaction would not remove that record.
    </P><P>
    This behavior is by design to prevent a complete removal of all records in instances of false positives or failures that impact all systems. It is often better to leave at least 1 system that has failed the monitor, rather than remove all records.
    </P><P>
    Once a monitor returns to a healthy status, the reaction will then re-Add all records it had previously removed.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'rec_name' : "www",
        'content' : '10.0.0.1'
   })



    email = TextField(
        "Email",
        description=BaseReactForm.descriptions['cloudflare']['email'],
        validators=[Email(message='Email address invalid')])
    domain = TextField(
        "Domain",
        description=BaseReactForm.descriptions['cloudflare']['domain'],
        validators=[DataRequired(message='Domain is a required field')])
    apikey = TextField(
        "API Key",
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    rec_name = TextField(
        "Record Name",
        description=BaseReactForm.descriptions['cloudflare']['recName']
    )
    content = TextField(
        "Record Content",
        description="""
          The Record Content is the IP or CNAME that should be removed while the reaction is executed and re-added when returning to normal
        """,
        validators=[DataRequired(message='Content is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
