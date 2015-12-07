######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import IPAddress, NumberRange
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
    ''' Class that creates a Reaction form for the dashboard '''
    title = "Heroku: Rollback Application Release"
    description = """
    <P>
      This reaction provides users with the ability for applications hosted on the Heroku platform to rollback to a previous release of the application. This reaction works by querying Heroku's API to determine the current application release. Every time this reaction is executed it will rollback the application by 1 release. This essentially provides the ability to continually rollback an application until the issue is resolved.
    </P>
    <P>
      The Minimum Release Version field is used to define a limit as to how far back the application releases can be reverted to. By setting this number to a known good release users are able to ensure their application version meets a minimal functionality.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
        'dynoname' : 'web.1',
        'min_release' : '150',
    })
    descriptions=BaseReactForm.descriptions

    apikey = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[
            DataRequired(message='API Key is a required field')
        ]
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
        validators=[
            DataRequired(message='Call On is a required field')
        ]
    )
    min_release = TextField(
        "Minimum Release Version",
        description="""
          Define a release to use as the furthest rollback point
        """,
        validators=[
            DataRequired(message="Minimum Release Version is a required field"),
            NumberRange(
                min=1,
                max=None, 
                message="Must be a number between 1 - 99999"
            )
        ]
    )


if __name__ == '__main__':
    pass
