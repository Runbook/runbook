######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange

class SubscribeForm(Form):
  ''' Class that creates signup form fields and validation '''
#  stripeToken = HiddenField("stripeToken", validators=[DataRequired(message='Uh Oh, something went wrong.')])
  stripeToken = HiddenField("stripeToken")
##  ccnum = TextField("Card Number")
##  cvc = TextField("CVC")
##  exp_month = TextField("MM")
##  exp_year = TextField("YYYY")

class AddPackForm(Form):
  ''' Class that creates signup form fields and validation '''
  add_packs = TextField("Additional Monitor Packages", validators=[NumberRange(min=0, message="Additional Monitor Packages must be a number")])

if __name__ == '__main__':
  pass
