"""Reaction form for DigitalOcean - Create new droplet."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):


    title = "DigitalOcean: Create new Droplet"
    description = """
    <P>
      This reaction provides the ability to create a new DigitalOcean Droplet when called. When creating the droplet this reaction will use the "Name Prefix" field and a timestamp as the droplet name. This is to allow the reaction to create a new droplet each time it is executed.
    </P><P>
      Use this reaction to increase capacity, provision an on-demand secondary server, or simply build a new server. When combined with automated provisioning tools, this reaction can provide very useful functionality.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'dropletid' : '12345',
        'name_prefix' : 'WebServer',
        'api_key' : placeholders['apikey'],
        'region' : 'nyc3',
        'size' : '512mb',
        'image' : 'ubuntu-14-04-x64',
        'ssh_keys' : 'key01',
    })

    api_key = TextField(
        'API Key',
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired('API Key is a required field.')])
    name_prefix = TextField(
        'Name Prefix',
        description=BaseReactForm.descriptions['digitalocean']['nameprefix'],
        validators=[DataRequired(message='Name prefix is a required field.')])
    region = TextField(
        'Region',
        description=BaseReactForm.descriptions['digitalocean']['region'],
        validators=[DataRequired(message='Region is a required field.')])
    size = TextField(
        'Size',
        description=BaseReactForm.descriptions['digitalocean']['size'],
        validators=[DataRequired(message='Size is a required field.')])
    image = TextField(
        'Image',
        description=BaseReactForm.descriptions['digitalocean']['image'],
        validators=[DataRequired(message='Image is a required field.')])
    ssh_keys = TextAreaField(
        'SSH Keys',
        description=BaseReactForm.descriptions['digitalocean']['sshkeys'],
        validators=[Optional()])
    backups = SelectField(
        'Enable Backups',
        description=BaseReactForm.descriptions['digitalocean']['backups'],
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()])
    ipv6 = SelectField(
        'IPV6 Networking',
        description=BaseReactForm.descriptions['digitalocean']['ipv6'],
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()],
    )
    private_networking = SelectField(
        'Enable Private Networking',
        description=BaseReactForm.descriptions['digitalocean']['privatenetworking'],
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        coerce=bool,
        validators=[Optional()],
    )
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])
