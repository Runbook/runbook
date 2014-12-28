######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class for PagerDuty notification
######################################################################

from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''

    subdomain = TextField(
        "Subdomain",
        validators=[DataRequired(message="Subdomain is a required field")])
    api_key = TextField(
        "API Key",
        validators=[DataRequired(message="API Key is a required field")])
    service_key = TextField(
        "Service Key",
        validators=[DataRequired(message='Service Key is a required field')])
    incident_key = TextField(
        "Incident Key",
        validators=[Optional()])
    description = TextField(
        "Description",
        validators=[DataRequired(message="Description is a required field")])
    details = TextAreaField(
        "Details",
        validators=[DataRequired(message="Details is a required field")])
    call_on = SelectField(
        "Call On",
        choices=[
        ('false', 'False Monitors'),
        ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])



if __name__ == '__main__':
    pass
