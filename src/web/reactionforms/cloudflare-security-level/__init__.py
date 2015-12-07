from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Email, IPAddress, NumberRange

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a CloudFlare Reaction form for the dashboard '''
    title = "CloudFlare: Change Security Level"
    description = """
    <P>
      This reaction is designed to modify the security level of a CloudFlare protected domain. When called, this reaction will interface with CloudFlare's API changing the domain's security level to the specified level.
    </P><P>
      The ability to increase the security level can be extremely useful when combined with logging service monitors that can be used to detect potential attacks.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'rec_name' : "www",
        'content' : '10.0.0.1'
   })


    actions = [
        ('essentially_off', 'Essentially Off'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('under_attack', 'Help I am under attack!')
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
    action = SelectField(
        "Level",
        description="""
          Specify the desired security level for the CloudFlare protected domain
        """,
        choices=actions,
        validators=[DataRequired(message='Security Level is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
