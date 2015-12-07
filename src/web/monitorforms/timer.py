######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Timer Forms Class
######################################################################

from wtforms import SelectField
from wtforms.validators import DataRequired
from base import BaseCheckForm


class TimerCheckForm(BaseCheckForm):

    ''' Class that creates an timer form for the dashboard '''
    timer = SelectField(
        "Interval",
        description="""
            Select how often you would like this monitor to be executed
        """,
        validators=[DataRequired(message="Interval is a required field")])

if __name__ == '__main__':
    pass
