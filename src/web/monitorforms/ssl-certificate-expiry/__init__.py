# SSL Certificate expiry check form.

from wtforms import IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange

from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):
    """Creates a wtforms object for SSL Certificate check monitor."""

    hostname = TextField(
        'Host name',
        validators=[DataRequired(message='Host name is a required field.')])
    port = IntegerField(
        'Port number',
        validators=[NumberRange(
            min=1, max=65536, message='Port number betweeen 1-65536')])
    num_days = IntegerField(
        'Days before cert expiration a warning should be generated.',
        validators=[NumberRange(
            min=1, max=365, message='Warning threshold between 1 - 365 days')])

if __name__ == '__main__':
    pass
