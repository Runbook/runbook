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
    title = "Heroku: Create Dyno"
    description = """
    <P>
      This reaction allows you to create a Heroku Dyno. This reaction allows users to specify the size and command for the created Dyno.
    </P>
    <P>
      The ability to create an Heroku Dyno is very powerful for Heroku users. This Dyno could be used to run a database script, clear an application queue, or any other maintenance type activities. Providing a simple way to automatically resolve many different types of issues.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
    })

    apikey = TextField("API Key",
                       description=BaseReactForm.descriptions['apikey'],
                       validators=[DataRequired(message='API Key is a required field')])
    appname = TextField("Application Name",
                        description=BaseReactForm.descriptions['heroku']['appname'],
                        validators=[DataRequired(message='Application Name is a required field')])
    call_on = SelectField("Call On",
                          description=BaseReactForm.descriptions['callon'],
                          choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
                          validators=[DataRequired(message='Call On is a required field')])


    cmd = TextField("Command",
                    description=BaseReactForm.descriptions['heroku']['cmd'],
                    validators=[DataRequired(message='Command is a required field')])
    attach = SelectField("Attach",
                         description=BaseReactForm.descriptions['heroku']['attach'],
                         choices=[('true', 'True'), ('false', 'False')],
                         validators=[DataRequired(message='Attach is a required field')])
    size = SelectField("Size",
                       description=BaseReactForm.descriptions['heroku']['size'],
                       choices=[('1X', '1X'), ('2X', '2X'), ('PX', 'PX')],
                       validators=[DataRequired(message='Size is a required field')])


if __name__ == '__main__':
    pass
