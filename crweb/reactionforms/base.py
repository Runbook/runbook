######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Base Reaction Form
######################################################################

from wtforms import Form
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange

class BaseReactForm(Form):
  ''' Class that creates a Base Reaction form for import '''
  name = TextField("Name", validators=[DataRequired(message='Name is a required field')])
  trigger = IntegerField("Trigger", validators=[NumberRange(min=0, max=999, message='Trigger must be a number between 0 - 999')])
  frequency = IntegerField("Frequency", validators=[NumberRange(min=0, max=999999999, message='Frequency must be a number between 0 - 999999999')])

if __name__ == '__main__':
  pass
