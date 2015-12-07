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
    title = "PagerDuty: Create Incident"
    description = """
    <P>
      This reaction provides the ability to create a PagerDuty incident. This functionality allows for automated incident creation based on monitor status.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'subdomain' : 'yourcompany',
        'api_key' : placeholders['apikey'],
        'service_key' : 'abc1342_121a',
        'incident_key' : 'Runbook Triggered Alert',
        'incident_description' : "Runbook Monitor detected failure",
        'details' : "HTTP Monitor returned a non-200 response",
    })
    descriptions=BaseReactForm.descriptions


    subdomain = TextField(
        "Subdomain",
        description="""
            Provide the SubDomain associated with your PagerDuty account
        """,
        validators=[DataRequired(message="Subdomain is a required field")])
    api_key = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[DataRequired(message="API Key is a required field")])
    service_key = TextField(
        "Service Key",
        description="""
            Provide the GUID Service key provided by PagerDuty
        """,
        validators=[DataRequired(message='Service Key is a required field')])
    incident_key = TextField(
        "Incident Key",
        description="""
            A unique string that serves as a unique Incident name/key
        """,
        validators=[Optional()])
    incident_description = TextField(
        "Description",
        description="""
            Provide a short description of the event
        """,
        validators=[DataRequired(message="Description is a required field")])
    details = TextAreaField(
        "Details",
        description="""
            Provide in depth details for the PagerDuty incident
        """,
        validators=[DataRequired(message="Details is a required field")])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[
        ('false', 'False Monitors'),
        ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])



if __name__ == '__main__':
    pass
