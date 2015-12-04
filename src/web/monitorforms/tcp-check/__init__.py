######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# TCP Health Check - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import IPAddress, NumberRange, DataRequired
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Class that creates an TCP Check form for the dashboard '''
    title = "TCP Port"
    description = """
    This monitor attempts to establish a TCP connection to the defined IP/Hostname and Port. If the connection is successfully established than the monitor will return True. If the connection cannot be established after 3 seconds the monitor is set as False.
    """
    placeholders = DatacenterCheckForm.placeholders
    ip = TextField(
        "IP",
        description=DatacenterCheckForm.descriptions['hostorip'],
        validators=[DataRequired(
            message='IP or Hostname is required')])
    port = TextField(
        "Port",
        description=DatacenterCheckForm.descriptions['port'],
        validators=[NumberRange(
            message='Port must be a number between 1 and 65535')])

if __name__ == '__main__':
    pass
