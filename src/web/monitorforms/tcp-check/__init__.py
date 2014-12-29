######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# TCP Health Check - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import IPAddress, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Class that creates an TCP Check form for the dashboard '''
    ip = TextField(
        "IP",
        validators=[IPAddress(
            message='Does not match IP address format')])
    port = TextField(
        "Port",
        validators=[NumberRange(
            message='Port must be a number between 1 and 65535')])

if __name__ == '__main__':
    pass
