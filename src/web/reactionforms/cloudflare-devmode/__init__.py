from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Email, IPAddress, NumberRange

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' wtform for CloudFlare Development Mode Reaction '''
    title = "CloudFlare: Change Development Mode"
    description = """
    This reaction gives you the ability to modify CloudFlare's development mode. Use this reaction to enable or disable CloudFlare's page cache on your domain during new application deployments or as a simple step during issues rending HTML pages.
    """

    actions = [
        ('off', 'Disable'),
        ('on', 'Enable')
    ]

    ''' Class that creates a CloudFlare Reaction form for the dashboard '''
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
    action = SelectField(
        "Action",
        description="""
          Define whether this reaction should Enable or Disable Development Mode
        """,
        choices=actions,
        validators=[DataRequired(message='Action is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
