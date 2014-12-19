"""Reactions form class for Nexmo SMS Notification."""

from wtforms import SelectField, TextField
from wtforms.validators import DataRequired
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    api_key = TextField(
        'api_key',
        validators=[DataRequired(message='API Key is a required field.')])
    api_secret = TextField(
        'api_secret',
        validators=[DataRequired(message='API Secret is a required field.')])
    from_address = TextField(
        'from_address',
        validators=[DataRequired(message='From Address is a required field.')])
    to_address = TextField(
        'to_address',
        validators=[DataRequired(message='To Address is a required field.')])
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
