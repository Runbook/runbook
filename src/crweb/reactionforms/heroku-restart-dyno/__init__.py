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
    apikey = TextField(
        "API Key",
        validators=[DataRequired(message='API Key is a required field')]
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
            ('failed', 'Failed Monitors'),
            ('healthy', 'Healthy Monitors')
        ],
        validators=[DataRequired(message='Call On is a required field')]
    )
    dynoname = TextField(
        "Dyno Name",
        validators=[DataRequired(message='Dyno Name is a required field')]
    )


if __name__ == '__main__':
    pass
