######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# HTTP Keyword Health Check - Forms Class
######################################################################

from wtforms import TextField, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL
from wtforms.widgets import TextArea
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

    title = "HTTP: Keyword Search"
    description = """
        This monitor will perform an HTTP GET request and search the returned data for a keyword. Keywords can be Regular Expressions or simple strings.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'keyword' : 'Could not connect to Database',
    })
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
        description = """
            Website or Application URL
        """,
        validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
    host = TextField(
        "Host Header",
        description = """
            Host header, allows users to make the request to a domain where the URL is different. For example a request to http://10.0.0.1 with a Host header of example.com will return the index for example.com
        """,
        validators=[DataRequired(message='Host header is a required field')])
    keyword = TextField(
        "Keyword",
        description = """
            Keyword to search for. This can be anything from a simple word to HTML code or Database Error 
        """,
        validators=[DataRequired(message='Keyword is a required field')])
    present = SelectField(
        "Presence",
        description = """
            If True the Monitor will be True when the Keyword is present and False when not. If set to False the monitor will be False when the Keyword is present.
        """,
        choices=present_choices,
        validators=[DataRequired(message='Present is a required field')])
    extra_headers = TextAreaField(
        'Additional HTTP Headers',
        description = """
            Use this field to add additional HTTP headers. Values are in a : seperated Key:Value format.
        """,
        validators=[HeaderList()],
        )
    regex = SelectField(
        "Regex",
        description = """
            Specify whether the Keyword is a Regular Expression or not
        """,
        choices=regex_choices,
        validators=[DataRequired(message='Regex is a required field')])

if __name__ == '__main__':
    pass
