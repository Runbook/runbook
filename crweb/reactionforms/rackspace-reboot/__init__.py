######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Reaction - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required, URL
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
  ''' Class that creates a Reaction form for the dashboard '''

  resource_choices = [
    ('cloudServersOpenStack', 'Next Generation Cloud Server'),
    ('cloudServers', 'First Generation Cloud Server')]

  region_choices = [
    ('DFW', 'DFW'),
    ('ORD', 'ORD'),
    ('IAD', 'IAD'),
    ('LON', 'LON'),
    ('SYD', 'SYD'),
    ('HKG', 'HKG')]

  username = TextField("Username", validator=[DataRequired(message='Username is a required field')])
  apikey = TextField("API Key", validators=[DataRequired(message='API Key is a required field')])
  serverid = TextField("Server ID#", validators=[DataRequired(message='Server ID# is a required field')])
  region = SelectField("Region", choices=region_choices, validators=[DataRequired(message="Select a Region")])
  resource_type = SelectField("Server Type", choices=resource_choices, validators=[DataRequired(message="Select a Server Type")])
  call_on = SelectField("Call On", choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')], validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
  pass
