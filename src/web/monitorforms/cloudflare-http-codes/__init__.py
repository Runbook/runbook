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
    title = "CloudFlare: HTTP Status Codes"
    description = """
    This monitor utilizes CloudFlare's zone analyitics to detect an increase in a specified set of HTTP Status Codes. This monitor can be used to identify increases in error or success codes. The threshold setting allows you to define the desired limit of the specified status codes.
    As zone analytics are determined by your CloudFlare plan, any time span less than 1 hour will require a CloudFlare Pro account or better.
    """
    webhook_include = "monitors/webhooks/general.html"
    placeholders = DatacenterCheckForm.placeholders

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
        ("505", '505 - HTTP version not supported'),
        ("520", '520 - Web server is returning an unknown error'),
        ("521", '521 - Web server is down'),
        ("522", '522 - Connection timed out'),
        ("523", '523 - Origin is unreachable'),
        ("524", '524 - A timeout occurred'),
        ("525", '525 - SSL handshake failed'),
        ("526", '526 - Invalid SSL certificate')
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
        description="""
            The email used to identify your CloudFlare account
        """,
        validators=[Email(message='Email address invalid')])
    domain = TextField(
        "Domain",
        description="""
           The domain you wish to perform this action on
        """,
        validators=[DataRequired(message='Domain is a required field')])
    apikey = TextField(
        "API Key",
        description="""
            Your CloudFlare API Key
        """,
        validators=[DataRequired(message='API Key is a required field')])
    threshold = TextField(
        "Threshold",
        description="""
            A number between 1 and 100 that defines a high water mark for this monitor
        """,
        validators=[DataRequired(message='Threshold is a required field'), NumberRange(min=1, message="Threshold must be a number between 1 - 100") ])
    codes = SelectMultipleField(
        "Codes",
        description="""
            Select one or more HTTP status codes to match against
        """,
        choices=choices,
        validators=[DataRequired(message='Codes is a required field')])
    start_time = SelectField(
        "Time Span",
        description="""
            Select the time intervals to validate against. For example if you wish to see 500 errors over the course of 15 minutes this setting should be 15 minutes.
        """,
        choices=start_choices,
        default="-1440",
        validators=[DataRequired(message="Time Span is a required field")])
    return_value = SelectField(
        "Return Value",
        description="""
            Select the returned value when this monitor is triggered. This allows you to specify whether the monitor should be True or False under the defined conditions.
        """,
        choices=return_choices,
        validators=[DataRequired(message="Return Value is a required field")])

if __name__ == '__main__':
    pass
