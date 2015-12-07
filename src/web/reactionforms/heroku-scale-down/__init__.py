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
    title = "Heroku: Scale Down"
    description = """
    <P>
        This reaction is designed to allow users to automatically Scale Down Heroku Dynos. The idea behind this reaction is to scale back Heroku infrastructure when traffic or workload decreases.
    </P>
    <P>
        The reaction is designed to reduce the size of existing Dynos, for example changing a Dyno's size from PX to 2X. The Minimum Size field allows users to define the lowest size the Dynos can be scaled down to, allowing for a minimal capacity to be defined.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
        'dynoname' : 'web.1',
        'dyno_type' : 'worker',
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
    min_size = SelectField("Minimum Size",
                           description="""
                             Select the lowest Dyno size acceptable
                           """,
                           choices=[( '1', '1X'), ( '2', '2X'), ( '3', 'PX')], validators=[DataRequired(message='Minimum Size is a required field')])


if __name__ == '__main__':
    pass
