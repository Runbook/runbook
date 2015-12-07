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
    title = "Heroku: Scale Up"
    description = """
    <P> 
      This reaction is designed to provide the ability to automatically scale up Heroku Dynos. By increasing a Dyno's size that single Dyno can then provide higher performance and capacity. This reaction works by querying the current Dyno size for the Dyno Type defined and increasing the size to the next value. The Maximum Size field allows users to define a limit as to the size Dyno's can be increased to.
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
    max_size = SelectField("Max Size",
                           description="""
                              Select the largest size this reaction should set
                           """,
                           choices=[( '1', '1X'), ( '2', '2X'), ( '3', 'PX')], validators=[DataRequired(message='Max Size is a required field')])


if __name__ == '__main__':
    pass
