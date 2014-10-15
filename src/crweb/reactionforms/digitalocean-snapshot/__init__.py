######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################


from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, NumberRange
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''

    apikey = TextField(
        "API Key",
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        "Droplet ID#",
        validators=[DataRequired(message='Droplet ID# is a required field'), NumberRange(min=1, max=None, message="Droplet ID should be a numeric ID number")])
    snapname = TextField(
        "Snapshot Name",
        validators=[DataRequired(message='Snapshot Name is a required field')])
    call_on = SelectField(
        "Call On",
        choices=[('failed', 'Failed Monitors'), ('healthy', 'Healthy Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
