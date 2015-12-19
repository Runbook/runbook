######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Timer Forms Class
######################################################################

from wtforms import SelectMultipleField
from wtforms.validators import DataRequired
from timer import TimerCheckForm
from web import app
from random import sample

class DatacenterCheckForm(TimerCheckForm):

    ''' Class that creates an datacenter form for the dashboard '''
    dc_choices = app.config['DATACENTERS']['choices']

    defaults = []
    if len(dc_choices) > 1:
        sampling = sample(dc_choices, 2)
        for item in sampling:
            defaults.append(item[0])
    else:
        defaults.append(dc_choices)
    

    datacenter = SelectMultipleField(
        "Data Center",
        description="""
            Select two or more Monitoring Zones where this monitor will be executed from
        """,
        choices=dc_choices,
        default=defaults,
        validators=[DataRequired(
            message='Monitoring Zone is a required field')])

if __name__ == '__main__':
    pass
