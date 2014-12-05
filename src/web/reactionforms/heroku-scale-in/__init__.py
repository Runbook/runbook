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

    dyno_type = TextField("Dyno Type", validators=[DataRequired(message='Dyno Type is a required field')])
    min_quantity = TextField("Minimum Dynos", validators=[DataRequired(message="Minimum Dyno is a required field"), NumberRange(min=1, max=None, message="Must be a number between 1 - 99999")])


if __name__ == '__main__':
    pass
