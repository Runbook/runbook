"""Reaction form for DigitalOcean - Create new droplet."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    api_key = TextField(
        'api_key',
        validators=[DataRequired('API Key is a required field.')])
    name_prefix = TextField(
        'name_prefix',
        validators=[DataRequired(message='Name prefix is a required field.')])
    region = TextField(
        'region',
        validators=[DataRequired(message='Region is a required field.')])
    size = TextField(
        'size',
        validators=[DataRequired(message='Size is a required field.')])
    image = TextField(
        'image',
        validators=[DataRequired(message='Image is a required field.')])
    ssh_keys = TextAreaField(
        'ssh_keys',
        validators=[Optional()])
    backups = SelectField(
        'backups',
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()])
    ipv6 = SelectField(
        'ipv6',
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()],
    )
    private_networking = SelectField(
        'private_networking',
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()],
    )
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])
