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
    title = "CloudFlare: Remove Record"
    description = """
    <P>
    This reaction is designed to simply remove a specified DNS record using CloudFlare's API. If the "Record Name" field is left blank, this reaction will remove all records that match the specified "Record Content". If the "Record Name" exists, than only that specific record will be removed.
    </P><P>
    The records removed via this reaction are not restored or retained. They are simply removed and no other action will take place.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'rec_name' : "www",
        'content' : '10.0.0.1'
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
    rec_name = TextField(
        "Record Name",
        description=BaseReactForm.descriptions['cloudflare']['recName']
    )
    content = TextField(
        "Record Content",
        description="""
          The Record Content is the IP or CNAME that should be removed
        """,
        validators=[DataRequired(message='Content is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
