######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Datadog Webhook Health Check - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseCheckForm

class CheckForm(BaseCheckForm):
  ''' Class that creates an TCP Check form for the dashboard '''
  pass

if __name__ == '__main__':
  pass
