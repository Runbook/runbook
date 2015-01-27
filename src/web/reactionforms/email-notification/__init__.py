"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Email
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    to_address = TextField(
        'to_address',
        validators=[DataRequired(message='To Address is a required field.'),
                    Email(message='Invalid Email Address.')])
    subject = TextField(
        'subject',
        validators=[DataRequired(message='Subject is a required field.')])
    body = TextAreaField(
        'body',
        validators=[DataRequired(message='Body is a required field.')])
    call_on = SelectField(
        'Call On',
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
