######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Timer Forms Class
######################################################################

from wtforms import SelectMultipleField
from wtforms.validators import DataRequired
from timer import TimerCheckForm


class DatacenterCheckForm(TimerCheckForm):

    ''' Class that creates an datacenter form for the dashboard '''
    dc_choices = [
        ("dc1queue", 'DigitalOcean - nyc2'),
        ("dc2queue", 'DigitalOcean - sfo1')
    ]

    datacenter = SelectMultipleField(
        "Datacenter",
        choices=dc_choices,
        validators=[DataRequired(
            message='Monitoring Zone is a required field')])

if __name__ == '__main__':
    pass
