"""Reaction form for HTTP GET / POST requests."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
from ..base import BaseReactForm
from ..utils import HeaderList


class PayloadValidator(object):

    def __call__(self, form, field):
        payload = str(field.data).strip()
        verb = form.http_verb.data
        if payload and verb not in ('POST',):
            raise ValidationError('Payload is not allowed with HTTP %s.' % verb)


class ReactForm(BaseReactForm):

    http_verb = SelectField(
        'http_verb',
        choices=[('GET', 'GET'), ('POST', 'POST')],
        default='GET',
        validators=[Optional()])
    url = TextField(
        'url',
        validators=[DataRequired(message='URL is a required field.'),
                    URL(message='Invalid URL format.')])
    extra_headers = TextAreaField(
        'extra_headers',
        validators=[HeaderList()])
    payload = TextAreaField(
        'payload',
        validators=[PayloadValidator()])
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])
