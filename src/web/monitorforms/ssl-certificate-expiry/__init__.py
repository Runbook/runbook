# SSL Certificate expiry check form.

from wtforms import IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange

from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):
    """Creates a wtforms object for SSL Certificate check monitor."""
    title = "SSL: Certificate Expiration"
    description = """
This monitor will connect to a specified port on a specified Hostname/IP and validate the provided SSL Certificate is not expired. This monitor returns a False value if the expiration date is less than the "Number of Days" away. For example this monitor will be False 4 days from expiration date if the threshold is set to 5 and True 6 days from expiration date.
    """

    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'num_days' : '5',
    })

    hostname = TextField(
        'Host',
        description="""
            The hostname or IP address of the system to check
        """,
        validators=[DataRequired(message='Hostname is a required field.')])
    port = IntegerField(
        'Port',
        description="""
            The port number to connect to for SSL validation
        """,
        validators=[NumberRange(
            min=1, max=65536, message='Port number betweeen 1-65536')])
    num_days = IntegerField(
        'Number of Days',
        description="""
            Define the threshold of days before expiration to trigger monitor
        """,
        validators=[NumberRange(
            min=1, max=365, message='Warning threshold between 1 - 365 days')])

if __name__ == '__main__':
    pass
