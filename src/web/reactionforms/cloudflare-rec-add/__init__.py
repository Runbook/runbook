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
    title = "CloudFlare: Record Add"
    description = """
    <P>
    This Reaction is designed to allow users to add a new DNS record to their CloudFlare protected domain's DNS zone. The reaction supports multiple types of records including A and CNAME records.
    </P><P>
    A great example of this reaction in use is to add extra capacity to your environment. Whether it is adding an additional server during peak load or adding a high priority MX server during failover.
    </p>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'rec_name' : "www",
        'content' : '10.0.0.1',
        'ttl' : '1',
   })


    type_of_recs = [
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('CNAME', 'CNAME'),
        ('TXT', 'TXT'),
        ('SRV', 'SRV'),
        ('LOC', 'LOC'),
        ('MX', 'MX'),
        ('NS', 'NS'),
        ('SPF', 'SPF')
    ]

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
    rec_type = SelectField(
        "Record Type",
        description=BaseReactForm.descriptions['cloudflare']['recType'],
        choices=type_of_recs,
        validators=[DataRequired(message='Record Type is a required field')])
    rec_name = TextField(
        "Record Name",
        description=BaseReactForm.descriptions['cloudflare']['recName'],
        validators=[DataRequired(message='Record Name is a required field')])
    content = TextField(
        "Record Content",
        description=BaseReactForm.descriptions['cloudflare']['content'],
        validators=[DataRequired(message='Content is a required field')])
    ttl = TextField(
        "TTL",
        description=BaseReactForm.descriptions['cloudflare']['ttl'],
        validators=[DataRequired(message='TTL is a required field')])
    proxied = SelectField(
        "Proxied",
        description=BaseReactForm.descriptions['cloudflare']['proxied'],
        choices=[("true", 'True'), ("false", 'False')],
        validators=[DataRequired(message='Proxied is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
