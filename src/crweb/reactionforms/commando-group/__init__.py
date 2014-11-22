######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Services Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Saltstack Reaction form for the dashboard '''

    recipe_id = TextField(
        "Recipe ID",
        validators=[DataRequired(message='Recipe ID is a required field')])
    group_id = TextField(
        "Group ID",
        validators=[DataRequired(message='Group ID is a required field')])
    halt_on_stderr = SelectField(
        "Halt on Error",
        choices=[('false', 'False'), ('true', 'True')],
        validators=[DataRequired(message='Halt on Error is a required field')])
    user = TextField(
        "User ID",
        validators=[DataRequired(message='User ID is a required field')])
    apikey = TextField(
        "API Key",
        validators=[DataRequired(message='API Key is a required field')])
    call_on = SelectField(
        "Call On",
        choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
