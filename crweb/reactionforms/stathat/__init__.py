######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## CloudFlare IP Replacement - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
  ''' Class that creates a CloudFlair Reaction form for the dashboard '''
  stat_name = TextField("Stat Name", validators=[DataRequired(message='Stat Name is a required field')])
  ez_key = TextField("EZ Key", validators=[DataRequired(message='EZ Key is a required field')])
  value = TextField("Value", validators=[NumberRange(message='Value must be a number')])
  continuous = SelectField("Continuous", choices=[('True', 'Yes'), ('False', 'No')], validators=[DataRequired(message='Continuous is a required field')])
  stat_type = SelectField("Stat Type", choices=[('count', 'Counter'), ('value', 'Value')], validators=[DataRequired(message='Stat Type is a required field')])
  call_on = SelectField("Call On", choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')], validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
  pass
