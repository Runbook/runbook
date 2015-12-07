######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Services Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Saltstack Reaction form for the dashboard '''
    title = "SaltStack: Download and Execute Script"
    description = """
    <P>
      This reaction provides a method for using Salt-API to trigger a <code>cmd.script</code> execution. This integration relies on the <a href="https://github.com/saltstack-formulas/salt-api-reactor-formula" target="_blank">Salt-API Reactor Formula</a> or a similar reactor and salt-api configuration to be in place. This reaction simply sends a webhook to the defined SaltStack API server.
    </P><P>
      SaltStack reactions open up many possible remediations, by integrating Runbook with SaltStack nearly any infrastructure task can be performed as a result of the integration.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'secretkey' : "OneTwoThree_VerySecret",
        'tgt' : "webserver*nyc3*.example.com",
        'args' : "--flags",
        'script' : "http://someaddress.com/script.sh",
    })
    descriptions=BaseReactForm.descriptions


    matcher_choices = [
        ("glob", "Hostname Glob"),
        ("pcre", "Hostname PCRE"),
        ("list", "List"),
        ("grain", "Grains"),
        ("grain_pcre", "Grains PCRE"),
        ("pillar", "Pillar"),
        ("nodegroup", "NodeGroup"),
        ("ipcidr", "IP Address/CIDR"),
        ("compound", "Compound")
    ]

    url = TextField(
        "URL",
        description=descriptions['url'],
        validators=[URL(message='URL must be in an appropriate format')])
    secretkey = TextField(
        "Secret Key",
        description=descriptions['saltstack']['secretkey'],
        validators=[DataRequired(message='Secret Key is a required field')])
    tgt = TextField(
        "Target",
        description=descriptions['saltstack']['tgt'],
        validators=[DataRequired(message='Target is a required field')])
    matcher = SelectField("Matcher",
                          description=descriptions['saltstack']['matcher'],
                          choices=matcher_choices,  validators=[
                          DataRequired(message='Matcher is a required field')])
    script = TextField(
        "Script",
        description="Provide a script to execute on the target system. This can either be an http:// or salt:// address.",
        validators=[DataRequired(message='Script is a required field')])
    args = TextField("Arguments", description="Provide arguments to the script being executed")
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
