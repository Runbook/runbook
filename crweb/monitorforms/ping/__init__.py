######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Ping Health Check - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo, Regexp
from ..datacenter import DatacenterCheckForm
import re

class CheckForm(DatacenterCheckForm):
  ''' Class that creates an Ping Health Check form for the dashboard '''
  pattern = "^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$"
  host = TextField("host", validators=[DataRequired(message='Host is a required field and should be a hostname or IP address'), Regexp(pattern, message="Invalid IP or Hostname format")])

if __name__ == '__main__':
  pass
