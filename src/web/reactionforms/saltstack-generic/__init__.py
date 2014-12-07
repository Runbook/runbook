######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Generic Modules - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Saltstack Reaction form for the dashboard '''

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
        validators=[URL(message='URL must be in an appropriate format')])
    secretkey = TextField(
        "Secret Key",
        validators=[DataRequired(message='Secret Key is a required field')])
    module = TextField(
        "Module",
        validators=[DataRequired(message='Module is a required field')])
    tgt = TextField(
        "Target",
        validators=[DataRequired(message='Target is a required field')])
    matcher = SelectField(
        "Matcher",
        choices=matcher_choices,
        validators=[DataRequired(message='Matcher is a required field')])
    args = TextField("Arguments")
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

    misc1 = TextField("Misc. #1")
    misc2 = TextField("Misc. #2")
    misc3 = TextField("Misc. #3")
    misc4 = TextField("Misc. #4")


if __name__ == '__main__':
    pass
