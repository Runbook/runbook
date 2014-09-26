######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## HTTP Keyword Health Check - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo, URL
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):
  ''' Class that creates an HTTP Get Status Code form for the dashboard '''

  present_choices = [
    ( "True", "True"),
    ( "False", "False")
  ]

  regex_choices = [
    ( "True", "True"),
    ( "False", "False")
  ]

  url = TextField("URL", validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
  host = TextField("Host", validators=[DataRequired(message='Host header is a required field')])
  keyword = TextField("Keyword", validators=[DataRequired(message='Keyword is a required field')])
  present = SelectField("Present", choices=present_choices, validators=[DataRequired(message='Present is a required field')])
  regex = SelectField("Regex", choices=regex_choices, validators=[DataRequired(message='Regex is a required field')])

if __name__ == '__main__':
  pass
