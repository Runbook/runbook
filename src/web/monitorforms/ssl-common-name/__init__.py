# SSL Certificate CN check form.

from wtforms import IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):
    """Creates a wtforms object for SSL Certificate check monitor."""
    title = "SSL: Check Common Name"
    description="""
        This monitor is used to monitor the common name for a specified SSL Certificate. If the common name of the SSL Certificate matches the specified common name this monitor will return True.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'expected_hostname' : 'www.example.com',
    })

    host = TextField(
        'Host',
        description = """
            Specify the hostname or IP address of the system whose SSL Certificate you wish to monitor.
        """,
        validators=[DataRequired(
            message='Host is a required field.')])
    port = IntegerField(
        'Port',
        description = """
            Specify the port number to connect to.
        """,
        validators=[NumberRange(
            min=1, max=65536, message='Port number betweeen 1-65536')])
    expected_hostname = TextField(
        'Common Name',
        description = """
            Specify the desired common name, any other common name results in a False monitor.
        """,
        validators=[DataRequired(
            message='Expected CN is a required field.')])


if __name__ == '__main__':
    pass
