######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, ValidationError, Required
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
    ''' Class that creates a Reaction form for the dashboard '''
    title = "Heroku: Restart Dyno"
    description = """
    <P>
      This reaction provides users with the ability to restart a Single Heroku Dyno. This reaction can be useful when needing to restart a critical Dyno or when the Heroku environment is relatively small.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
        'dynoname' : 'web.1',
    })
    descriptions=BaseReactForm.descriptions

    apikey = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')]
    )
    appname = TextField(
        "Application Name",
        description=descriptions['heroku']['appname'],
        validators=[
          DataRequired(message='Application Name is a required field')
        ]
    )
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[
            ('false', 'False Monitors'),
            ('true', 'True Monitors')
        ],
        validators=[DataRequired(message='Call On is a required field')]
    )
    dynoname = TextField(
        "Dyno Name",
        description=descriptions['heroku']['dynoname'],
        validators=[DataRequired(message='Dyno Name is a required field')]
    )


if __name__ == '__main__':
    pass
