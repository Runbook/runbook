######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''

    region = TextField(
        "AWS Region",
        validators=[DataRequired(message="AWS Region is a required field")])
    aws_access_key = TextField(
        "AWS Access Key",
        validators=[DataRequired(message='AWS Access Key is a required field')])
    aws_secret_key = TextField(
        "AWS Secret Key",
        validators=[DataRequired(message='AWS Secret Key is a required field')])
    instance_id = TextField(
        "Instance ID",
        validators=[DataRequired(message="Instance ID is a required field")])
    call_on = SelectField(
        "Call On",
        choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
