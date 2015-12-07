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
    title = "Heroku: Scale In"
    description = """
    <P>
        This reaction provides the ability to Scale In (reduce) the number of active Heroku Dynos. This reaction works by querying the current number of Dynos associated with the specified Dyno Type and reduces the number by 1. The Minimum Dynos field defines a restriction on how many Dynos can be reduced.
    </P>
    <P>
        This functionality provides a scaling capability that can be used to reduce unused or unneeded Heroku Dynos.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'appname' : 'StormyWaters58',
        'cmd' : 'bash script.sh',
        'dynoname' : 'web.1',
        'dyno_type' : 'worker',
        'min_quantity' : '12',
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
    min_quantity = TextField("Minimum Dynos",
                             description="""
                                Define the minimum number of Dynos to keep
                             """,
                             validators=[DataRequired(message="Minimum Dyno is a required field"), NumberRange(min=1, max=None, message="Must be a number between 1 - 99999")])


if __name__ == '__main__':
    pass
