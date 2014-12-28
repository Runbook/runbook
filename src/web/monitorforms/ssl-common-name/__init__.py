# SSL Certificate CN check form.

from wtforms import IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):
    """Creates a wtforms object for SSL Certificate check monitor."""

    host = TextField(
        'Host',
        validators=[DataRequired(
            message='Host is a required field.')])
    port = IntegerField(
        'Port',
        validators=[NumberRange(
            min=1, max=65536, message='Port number betweeen 1-65536')])
    expected_hostname = TextField(
        'Expected CN',
        validators=[DataRequired(
            message='Expected CN is a required field.')])


if __name__ == '__main__':
    pass
