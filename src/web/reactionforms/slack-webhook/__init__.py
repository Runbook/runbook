"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    url = TextField(
        'Webhook URL',
        validators=[DataRequired(message='The URL is a required field.'),
                    URL(message='Invalid URL Address.')])
    channel = TextField(
        'Channel',
        validators=[DataRequired(message='Channel is a required field.')])
    body = TextField(
        'Message',
        validators=[DataRequired(message='Message is a required field.')])
    call_on = SelectField(
        'Call On',
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
