######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Base Monitor Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectMultipleField
from wtforms.validators import DataRequired


class BaseCheckForm(Form):

    def __init__(self, *args, **kwargs):                                        
        super(BaseCheckForm,self).__init__(*args, **kwargs)                          

    ''' Class that creates an TCP Check form for the dashboard '''
    name = TextField(
        "Name",
        validators=[DataRequired(message='Name is a required field')],
        description="""
            A user defined name for the Runbook Monitor. Name can be alphanumeric and contain special characters.
        """,
    )
    reactions = SelectMultipleField(
        "Reactions",
        description="""
            Select the reaction or reactions you would like to execute with this monitor
        """,
    )

    # Common placeholder values
    placeholders = {
        'name' : 'Name',
        'email' : 'user@example.com',
        'domain' : 'example.com',
        'apikey' : 'API Key',
        'threshold' : '10',
        'hostname' : 'example.com',
        'host' : 'example.com',
        'url' : 'https://example.com/server-health',
        'extra_headers' : 'header:value',
        'port' : '443',
    }

    webhook_include = "monitors/webhooks/general.html"


if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
