######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## CloudFlare IP Replacement - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
  ''' Class that creates a CloudFlair Reaction form for the dashboard '''
  send_choices = [
                   ('False', 'No'),
                   ('True', 'Yes')]
  email = TextField("Email", validators=[Email(message='Email address invalid')])
  send_healthy = SelectField("Send When Healthy", choices=send_choices, validators=[DataRequired(message='You must select to send email when healthy or not')])

if __name__ == '__main__':
  pass
