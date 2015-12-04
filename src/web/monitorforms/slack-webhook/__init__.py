######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Health Check - Forms Class
######################################################################

from ..base import BaseCheckForm
from wtforms import TextField
from wtforms.validators import DataRequired
from ..datacenter import DatacenterCheckForm


class CheckForm(BaseCheckForm):
    ''' Class that creates an web form for the dashboard '''
    title = "Slack: Webhook"
    description = """
    The Slack Webhook monitor allows for integration with both Slack Commands and Slack Outbound Webhooks.
    """
    placeholders = DatacenterCheckForm.placeholders

    token = TextField(
        'Slack Token',
        description=DatacenterCheckForm.descriptions['token'],
        validators=[DataRequired(message='Slack Token is a required field')])

if __name__ == '__main__':
    pass
