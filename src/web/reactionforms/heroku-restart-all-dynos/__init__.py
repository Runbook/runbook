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
    title = "Heroku: Restart All Dynos"
    description = """
    <P>
      This reaction provides the ability to restart all Dynos within the specified Heroku Application. This reaction will send an API request to Heroku to restart all Dynos, the Dyno will be restarted whether it is already running or not. This reaction should only be used in events that cover a full failure or within environments that can tolerate the time it takes to restart Dynos.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
    })


    apikey = TextField(
        "API Key",
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')]
    )
    appname = TextField(
        "Application Name",
        description=BaseReactForm.descriptions['heroku']['appname'],
        validators=[
          DataRequired(message='Application Name is a required field')
        ]
    )
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[
            ('false', 'False Monitors'),
            ('true', 'True Monitors')
        ],
        validators=[DataRequired(message='Call On is a required field')]
    )


if __name__ == '__main__':
    pass
