######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# HTTP Keyword Health Check - Forms Class
######################################################################

from wtforms import TextField, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL
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
        except Exception:
            raise ValidationError('Invalid headers. Use key:value format.')


class CheckForm(DatacenterCheckForm):

    ''' Class that creates an HTTP Get Status Code form for the dashboard '''

    present_choices = [
        ("True", "True"),
        ("False", "False")
    ]

    regex_choices = [
        ("True", "True"),
        ("False", "False")
    ]

    url = TextField(
        "URL",
        validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
    host = TextField(
        "Host",
        validators=[DataRequired(message='Host header is a required field')])
    keyword = TextField(
        "Keyword",
        validators=[DataRequired(message='Keyword is a required field')])
    present = SelectField(
        "Present",
        choices=present_choices,
        validators=[DataRequired(message='Present is a required field')])
    extra_headers = TextAreaField(
        'extra_headers',
        validators=[HeaderList()])
    regex = SelectField(
        "Regex",
        choices=regex_choices,
        validators=[DataRequired(message='Regex is a required field')])

if __name__ == '__main__':
    pass
