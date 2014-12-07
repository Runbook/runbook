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

    apikey = TextField(
        "API Key",
        validators=[
            DataRequired(message='API Key is a required field')
        ]
    )
    appname = TextField(
        "Application Name",
        validators=[
            DataRequired(message='Application Name is a required field')
        ]
    )
    call_on = SelectField(
        "Call On",
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
