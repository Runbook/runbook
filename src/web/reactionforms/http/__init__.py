"""Reaction form for HTTP GET / POST requests."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
from ..base import BaseReactForm
from ..utils import http


class PayloadValidator(object):

    def __call__(self, form, field):
        payload = str(field.data).strip()
        verb = form.http_verb.data
        if payload and verb not in ('POST',):
            raise ValidationError('Payload is not allowed with HTTP %s.' % verb)


class ReactForm(BaseReactForm):
    title = "HTTP Request"
    description = """
    <P> 
      This reaction is designed to provide the ability to perform basic HTTP requests. When called this reaction will perform either an HTTP GET or HTTP POST request with the headers, and payload specified. This reaction could be used to perform arbitrary API calls, webhook requests, or anything else triggered by HTTP requests.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
      'payload' : "[{ 'json' : True }]"
    })
    descriptions=BaseReactForm.descriptions

    http_verb = SelectField(
        'HTTP Method',
        description=descriptions['http']['http_method'],
        choices=[('GET', 'GET'), ('POST', 'POST')],
        default='GET',
        validators=[Optional()])
    url = TextField(
        'URL',
        description=descriptions['http']['url'],
        validators=[DataRequired(message='URL is a required field.'),
                    URL(message='Invalid URL format.')])
    extra_headers = TextAreaField(
        'Extra Headers',
        description=descriptions['http']['extra_headers'],
        validators=[http.HeaderList()])
    payload = TextAreaField(
        'Request Payload',
        description=descriptions['http']['payload'],
        validators=[PayloadValidator()])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])
