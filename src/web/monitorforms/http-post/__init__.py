"""HTTP Post Form"""

from wtforms import TextAreaField, TextField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
from ..datacenter import DatacenterCheckForm


class HeaderList(object):
    """Custom wtform validator for headers."""

    def __call__(self, form, field):
        try:
            for header in str.splitlines(str(field.data)):
                header = header.strip()
                # Ignore empty lines
                if not header:
                    continue
                key, value = header.split(':')
                key = key.strip()
                value = value.strip()
                assert key
                assert value
        except Exception, e:
            raise ValidationError('Invalid headers. Use key:value format.')


class CheckForm(DatacenterCheckForm):

    url = TextField(
        'url',
        validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
    host = TextField(
        'host',
        validators=[DataRequired(message='Host header is a required field')])
    payload = TextAreaField(
        'payload',
        validators=[Optional()])
    extra_headers = TextAreaField(
        'extra_headers',
        validators=[HeaderList()])
    response_regex = TextField(
        'response_regex',
        validators=[Optional()])
    response_headers = TextAreaField(
        'response_headers',
        validators=[HeaderList()])


if __name__ == '__main__':
    pass
