######################################################################
## Cloud Routes Web Application
## -------------------------------------------------------------------
## Timer Forms Class
######################################################################

from wtforms import Form
from wtforms import SelectField
from wtforms.validators import DataRequired, ValidationError
from base import BaseCheckForm

class TimerCheckForm(BaseCheckForm):
  ''' Class that creates an timer form for the dashboard '''
  timer = SelectField("Interval", validators=[DataRequired(message="Interval is a required field")])

if __name__ == '__main__':
  pass
