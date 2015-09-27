######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# CloudFlare IP Replacement - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Email, IPAddress, NumberRange

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

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

    ''' Class that creates a CloudFlare Reaction form for the dashboard '''
    email = TextField(
        "Email",
        validators=[Email(message='Email address invalid')])
    domain = TextField(
        "Domain",
        validators=[DataRequired(message='Domain is a required field')])
    apikey = TextField(
        "APIKey",
        validators=[DataRequired(message='API Key is a required field')])
    rec_type = SelectField(
        "Record Type",
        choices=type_of_recs,
        validators=[DataRequired(message='Record Type is a required field')])
    rec_name = TextField(
        "Record Name")
    content = TextField(
        "Record Content",
        validators=[DataRequired(message='Content is a required field')])
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
