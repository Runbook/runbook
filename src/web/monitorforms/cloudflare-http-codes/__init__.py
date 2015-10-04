######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# HTTP Get Status Code Health Check - Forms Class
######################################################################

from wtforms import TextField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Class that creates an HTTP Get Status Code form for the dashboard '''

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

    return_choices = [
        ("true", "True"),
        ("false", "False")
    ]

    start_choices = [
        ("-30", "1 minute"),
        ("-360", "15 minutes"),
        ("-720", "30 minutes"),
        ("-1440", "1 hour"),
        ("-10080", "1 day")
    ]

    email = TextField(
        "Email",
        validators=[Email(message='Email address invalid')])
    domain = TextField(
        "Domain",
        validators=[DataRequired(message='Domain is a required field')])
    apikey = TextField(
        "APIKey",
        validators=[DataRequired(message='API Key is a required field')])
    threshold = TextField(
        "Threshold",
        validators=[DataRequired(message='Threshold is a required field'), NumberRange(min=1, message="Threshold must be a number between 1 - 100") ])
    codes = SelectMultipleField(
        "Codes",
        choices=choices,
        validators=[DataRequired(message='Codes is a required field')])
    start_time = SelectField(
        "Time Span",
        choices=start_choices,
        validators=[DataRequired(message="Time Span is a required field")])
    return_value = SelectField(
        "Return Value",
        choices=return_choices,
        validators=[DataRequired(message="Return Value is a required field")])

if __name__ == '__main__':
    pass
