######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# HTTP Get Status Code Health Check - Forms Class
######################################################################

from wtforms import TextField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Monitor form for cloudflare traffic increase monitoring '''
    title = "CloudFlare: Decrease in Traffic"
    description = """
    This monitor utilizes CloudFlare's zone analyitics to detect a decrease in HTTP requests. This monitor can be used to detect changes to HTTP traffic and be combined with scaling reactions. The threshold setting allows you to define the percentage of change to trigger on. For example; if more than 50% of the web traffic decreases trigger this monitor as True.
    """
    placeholders = DatacenterCheckForm.placeholders

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
        "CloudFlare Email",
        description=DatacenterCheckForm.descriptions['cloudflare']['email'],
        validators=[Email(message='Email address invalid')])
    domain = TextField(
        "Domain",
        description=DatacenterCheckForm.descriptions['domain'],
        validators=[DataRequired(message='Domain is a required field')])
    apikey = TextField(
        "API Key",
        description=DatacenterCheckForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    threshold = TextField(
        "Threshold",
        description = """
        Define the percentage of change to trigger this monitor on. If this monitor should be True when traffic decreases by 20% than the value here should be 20
        """,
        validators=[DataRequired(message='Threshold is a required field'), NumberRange(min=1, message="Threshold must be a number between 1 - 100") ])
    start_time = SelectField(
        "Time Span",
        description=DatacenterCheckForm.descriptions['cloudflare']['timespan'],
        choices=start_choices,
        validators=[DataRequired(message="Time Span is a required field")])
    return_value = SelectField(
        "Return Value",
        description=DatacenterCheckForm.descriptions['return_value'],
        choices=return_choices,
        validators=[DataRequired(message="Return Value is a required field")])

if __name__ == '__main__':
    pass
