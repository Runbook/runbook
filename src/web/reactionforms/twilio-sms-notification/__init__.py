"""Reactions form class for Twilio SMS Notification."""

from wtforms import SelectField, TextField
from wtforms.validators import DataRequired, Regexp
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    account_sid = TextField(
        'account_sid',
        validators=[DataRequired(message='Account SID is a required field.')])
    auth_token = TextField(
        'auth_token',
        validators=[DataRequired(message='Auth Token is a required field.')])
    from_address = TextField(
        'from_address',
        validators=[DataRequired(message='From Address is a required field.'),
                    Regexp('^\+?\d{5,}$', message='Invalid format for From Address. Use numbers only or international format (+123456789).')])
    to_address = TextField(
        'to_address',
        validators=[DataRequired(message='To Address is a required field.'),
                    Regexp('^\+?\d{5,}$', message='Invalid format for To Address. Use numbers only or international format (+123456789).')])
    text = TextField(
        'text',
        validators=[DataRequired(message='Message Text is a required field.')])
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
