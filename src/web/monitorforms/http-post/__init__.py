"""HTTP Post Form"""

from wtforms import SelectMultipleField, TextAreaField, TextField
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
        except Exception:
            raise ValidationError('Invalid headers. Use key:value format.')


class CheckForm(DatacenterCheckForm):

    ''' Form for creating the http post monitor '''
    title = "HTTP: Post"
    description = """
        This monitor will perform an HTTP POST request and either validate the status code, headers or response content. This Monitor is a useful for monitoring other services and web applications.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'payload' : 'POST Data',
        'response_regex' : '.*[s|S]uccess.*',
        'response_headers' : 'header:value',
    })

    choices = [
        ("100", '100 - Continue'),
        ("101", '101 - Switching protocols'),
        ("200", '200 - Successful'),
        ("201", '201 - Created'),
        ("202", '202 - Accepted'),
        ("203", '203 - Non-authoritative information'),
        ("204", '204 - No content'),
        ("205", '205 - Reset content'),
        ("206", '206 - Partial content'),
        ("300", '300 - Multiple choices'),
        ("301", '301 - Move permanently'),
        ("302", '302 - Moved temporarily'),
        ("303", '303 - See other location'),
        ("304", '304 - Not Modified'),
        ("305", '305 - Use proxy'),
        ("307", '307 - Temporary redirect'),
        ("400", '400 - Bad request'),
        ("401", '401 - Not authorized'),
        ("403", '403 - Forbidden'),
        ("404", '404 - Not found'),
        ("405", '405 - Method not allowed'),
        ("406", '406 - Not acceptable'),
        ("407", '407 - Proxy authentication required'),
        ("408", '408 - Request timeout'),
        ("409", '409 - Conflict'),
        ("410", '410 - Gone'),
        ("411", '411 - Length required'),
        ("412", '412 - Precondition failed'),
        ("413", '413 - Request entity too large'),
        ("414", '414 - Requested URI is too long'),
        ("415", '415 - Unsupported media type'),
        ("416", '416 - Requested range not satisfiable'),
        ("417", '417 - Expectation failed'),
        ("500", '500 - Internal server error'),
        ("501", '501 - Not implemented'),
        ("502", '502 - Bad gateway'),
        ("503", '503 - Service unavailable'),
        ("504", '504 - Gateway timeout'),
        ("505", '505 - HTTP version not supported')
    ]

    url = TextField(
        'URL',
        description="""
            The web address you wish to send the POST request to
        """,
        validators=[DataRequired(message='URL is a required field.'),
                    URL(message='Must be a url such as "https://127.0.0.1"')])
    host = TextField(
        'Host Header',
        description="""
            The Host header used to address a specific domain even when the URL is to another domain or IP address
        """,
        validators=[DataRequired(message='Host header is a required field')])
    payload = TextAreaField(
        'POST Data',
        description="""
            This section contains the POST data to be used when the monitor makes a request
        """,
        validators=[Optional()])
    extra_headers = TextAreaField(
        'Additional Headers',
        description="""
            Use this field to add additional HTTP headers. Values are in a : seperated Key:Value format.
        """,
        validators=[HeaderList()])
    status_codes = SelectMultipleField(
        'HTTP Status Codes',
        description="""
            Select the desired HTTP Status Codes
        """,
        choices=choices,
        validators=[Optional()])
    response_regex = TextField(
        'Keyword',
        description="""
            If defined this field will search for the specified keyword or regular expression
        """,
        validators=[Optional()])
    response_headers = TextAreaField(
        'Response Headers',
        description="""
            Validate the specified headers are provided in the HTTP response
        """,
        validators=[HeaderList()])


if __name__ == '__main__':
    pass
