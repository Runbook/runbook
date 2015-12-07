######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required, URL
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
    ''' Class that creates a Reaction form for the dashboard '''
    title = "Heroku: Scale Out"
    description = """
    <P>
        This reaction is designed to allow users to automatically scale their Heroku environment. This reaction works by querying the current number of Heroku Dyno's and increasing that number by 1. The number however, will not be increased beyond the Maximum Dynos value.
    </P>
    <P> 
        This functionality can be critical to meeting capacity requirements during large increases of traffic or other workloads.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
        'dynoname' : 'web.1',
        'dyno_type' : 'worker',
        'max_quantity' : '15',
    })
    descriptions=BaseReactForm.descriptions

    apikey = TextField("API Key",
                       description=descriptions['apikey'],
                       validators=[DataRequired(message='API Key is a required field')])
    appname = TextField("Application Name",
                        description=descriptions['heroku']['appname'],
                        validators=[DataRequired(message='Application Name is a required field')])
    call_on = SelectField("Call On",
                          description=descriptions['callon'],
                          choices=[('false', 'False Monitors'), ('true', 'True Monitors')], validators=[DataRequired(message='Call On is a required field')])

    dyno_type = TextField("Dyno Type",
                          description=descriptions['heroku']['dynotype'],
                          validators=[DataRequired(message='Dyno Type is a required field')])
    max_quantity = TextField("Maximum Dynos",
                             description="""
                                Define the maximum number of Dynos to scale to
                             """,
                             validators=[DataRequired(message="Maximum Dyno is a required field"), NumberRange(min=1, max=None, message="Must be a number between 1 - 99999")])


if __name__ == '__main__':
    pass
