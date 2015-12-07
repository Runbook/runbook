######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Keys - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Saltstack Reaction form for the dashboard '''
    title = "SaltStack: Manage Keys"
    description = """
    <P>
      This reaction provides a method for using Salt-API to accept, reject or delete a minion key. This integration relies on the <a href="https://github.com/saltstack-formulas/salt-api-reactor-formula" target="_blank">Salt-API Reactor Formula</a> or a similar reactor and salt-api configuration to be in place. This reaction simply sends a webhook to the defined SaltStack API server.
    </P><P>
      SaltStack reactions open up many possible remediations, by integrating Runbook with SaltStack nearly any infrastructure task can be performed as a result of the integration.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'secretkey' : "OneTwoThree_VerySecret",
        'minion' : "webserver*.example.com",
    })
    descriptions=BaseReactForm.descriptions

    function_choices = [
        ("accept", "Accept"),
        ("delete", "Delete"),
        ("reject", "Reject")
    ]

    url = TextField(
        "URL",
        description=descriptions['url'],
        validators=[URL(message='URL must be in an appropriate format')])
    secretkey = TextField(
        "Secret Key",
        description=descriptions['saltstack']['secretkey'],
        validators=[DataRequired(message='Secret Key is a required field')])
    function = SelectField(
        "Function",
        description="Select the action to perform",
        choices=function_choices,
        validators=[DataRequired(message='Function is a required field')])
    minion = TextField(
        "Minion",
        description="Provide a minion name or glob",
        validators=[DataRequired(message='Target is a required field')])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
