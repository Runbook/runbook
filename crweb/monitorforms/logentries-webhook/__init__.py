######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Health Check - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseCheckForm

class CheckForm(BaseCheckForm):
  ''' Class that creates an web form for the dashboard '''
  pass

if __name__ == '__main__':
  pass
