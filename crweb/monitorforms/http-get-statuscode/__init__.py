######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## HTTP Get Status Code Health Check - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo, URL
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):
  ''' Class that creates an HTTP Get Status Code form for the dashboard '''

  choices = [
    ( "100", '100 - Continue'),
    ( "101", '101 - Switching protocols'),
    ( "200", '200 - Successful'),
    ( "201", '201 - Created'),
    ( "202", '202 - Accepted'),
    ( "203", '203 - Non-authoritative information'),
    ( "204", '204 - No content'),
    ( "205", '205 - Reset content'),
    ( "206", '206 - Partial content'),
    ( "300", '300 - Multiple choices'),
    ( "301", '301 - Move permanently'),
    ( "302", '302 - Moved temporarily'),
    ( "303", '303 - See other location'),
    ( "304", '304 - Not Modified'),
    ( "305", '305 - Use proxy'),
    ( "307", '307 - Temporary redirect'),
    ( "400", '400 - Bad request'),
    ( "401", '401 - Not authorized'),
    ( "403", '403 - Forbidden'),
    ( "404", '404 - Not found'),
    ( "405", '405 - Method not allowed'),
    ( "406", '406 - Not acceptable'),
    ( "407", '407 - Proxy authentication required'),
    ( "408", '408 - Request timeout'),
    ( "409", '409 - Conflict'),
    ( "410", '410 - Gone'),
    ( "411", '411 - Length required'),
    ( "412", '412 - Precondition failed'),
    ( "413", '413 - Request entity too large'),
    ( "414", '414 - Requested URI is too long'),
    ( "415", '415 - Unsupported media type'),
    ( "416", '416 - Requested range not satisfiable'),
    ( "417", '417 - Expectation failed'),
    ( "500", '500 - Internal server error'),
    ( "501", '501 - Not implemented'),
    ( "502", '502 - Bad gateway'),
    ( "503", '503 - Service unavailable'),
    ( "504", '504 - Gateway timeout'),
    ( "505", '505 - HTTP version not supported')
  ]

  url = TextField("URL", validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
  host = TextField("Host", validators=[DataRequired(message='Host header is a required field')])
  codes = SelectMultipleField("Codes", choices=choices, validators=[DataRequired(message='Codes is a required field')])

if __name__ == '__main__':
  pass
