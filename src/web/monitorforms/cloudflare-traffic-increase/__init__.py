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
