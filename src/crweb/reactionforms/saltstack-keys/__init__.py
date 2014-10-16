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

    function_choices = [
        ("accept", "Accept"),
        ("delete", "Delete"),
        ("reject", "Reject")
    ]

    url = TextField(
        "URL",
        validators=[URL(message='URL must be in an appropriate format')])
    secretkey = TextField(
        "Secret Key",
        validators=[DataRequired(message='Secret Key is a required field')])
    function = SelectField(
        "Function",
        choices=function_choices,
        validators=[DataRequired(message='Function is a required field')])
    minion = TextField(
        "Target",
        validators=[DataRequired(message='Target is a required field')])
    call_on = SelectField(
        "Call On",
        choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
