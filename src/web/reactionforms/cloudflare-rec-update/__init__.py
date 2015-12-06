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
    title = "CloudFlare: Update Record"
    description = """
    <P>
      This reaction is designed to update an existing CloudFlare DNS record with new content. This reaction also provides the ability to replace one record type (such as an A record) with another (such as a CNAME record).
    </P><P>
      Similar to other CloudFlare reactions, if the "Record Name" field is missing this reaction will find all records with a matching Record Type and Record Content and update accordingly.      
    </P><P>
      This reaction can be used for Active-Passive failover by replacing the primary IP address with a secondary IP address. This reaction will not automatically revert changes, for this a second reaction should be created.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'rec_name' : "www",
        'content' : '10.0.0.1',
        'new_content' : '10.0.0.1'
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
    )
    content = TextField(
        "Record Content",
        description=BaseReactForm.descriptions['cloudflare']['content'],
        validators=[DataRequired(message='Content is a required field')])
    new_rec_type = SelectField(
        "New Record Type",
        description=BaseReactForm.descriptions['cloudflare']['recType'],
        choices=type_of_recs,
        validators=[DataRequired(message='New Record Type is a required field')])
    new_content = TextField(
        "New Record Content",
        description=BaseReactForm.descriptions['cloudflare']['content'],
        validators=[DataRequired(message='New Content is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
