######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# HTTP Get Status Code Health Check - Forms Class
######################################################################

from wtforms import TextField, SelectMultipleField, TextAreaField
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
    title = "HTTP GET Status Code"
    description = """
    This monitor will perform an HTTP GET request to the specified URL and verify that the returned Status Code matches the defined list. If the returned code is not found in the "Status Code" list, this monitor will return False. You can use this monitor to detect issues with Web applications. With the "Host" header it is possible to setup this monitor for an IP rather than a DNS name. Allowing users to monitor servers without using DNS.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'appname' : 'Application Name',
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
        "URL",
        description=DatacenterCheckForm.descriptions['url'],
        validators=[URL(message='Must be a url such as "https://127.0.0.1"')])
    host = TextField(
        "Host Header",
        description=DatacenterCheckForm.descriptions['host'],
        validators=[DataRequired(message='Host header is a required field')])
    codes = SelectMultipleField(
        "HTTP Status Codes",
        description=DatacenterCheckForm.descriptions['http_codes'],
        choices=choices,
        validators=[DataRequired(message='Codes is a required field')])
    extra_headers = TextAreaField(
        'Extra HTTP Headers',
        description=DatacenterCheckForm.descriptions['extra_headers'],
        validators=[HeaderList()])

if __name__ == '__main__':
    pass
