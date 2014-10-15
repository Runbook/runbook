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

    apikey = TextField("API Key", validators=[DataRequired(message='API Key is a required field')])
    appname = TextField("Application Name", validators=[DataRequired(message='Application Name is a required field')])
    call_on = SelectField("Call On", choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')], validators=[DataRequired(message='Call On is a required field')])


    cmd = TextField("Command", validators=[DataRequired(message='Command is a required field')])
    attach = SelectField("Attach", choices=[('true', 'True'), ('false', 'False')], validators=[DataRequired(message='Attach is a required field')])
    size = SelectField("Size", choices=[('1X', '1X'), ('2X', '2X'), ('PX', 'PX')], validators=[DataRequired(message='Size is a required field')])


if __name__ == '__main__':
    pass
