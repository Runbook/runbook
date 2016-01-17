"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    ''' Class that creates an form for the reaction '''
    title = "Linux: Manage Services"
    description = """
    <p>This reaction will open an SSH connection to the specified host and performs the specified action on the specified service.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the reaction to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({'service_name' : 'nginx'})
    field_descriptions = BaseReactForm.descriptions
    actions = [
        ('restart', 'Restart'),
        ('start', 'Start'),
        ('stop', 'Stop'),
        ('reload', 'Reload')
    ]


    service_name = TextField(
        "Service",
        description="""
          The service you wish to perform this action against in the same format you would execute systemctl or service commands with.
        """,
        validators=[DataRequired(message='Service is a required field')])
    action = SelectField(
        "Action",
        description="""
          Action to perform against the specified service.
        """,
        choices=actions,
        validators=[DataRequired(message="Action is a required field")])

    host_string = TextField(
        "Target Host",
        description=field_descriptions['ssh']['host_string'],
        validators=[DataRequired(message='Target Host is a required field')])
    gateway = TextField(
        "Gateway Host",
        description=field_descriptions['ssh']['gateway'],
        validators=[Optional()])
    username = TextField(
        "Username",
        description=field_descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=field_descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    use_sudo = SelectField(
        "Use Sudo",
        description=field_descriptions['ssh']['use_sudo'],
        choices=[('true', 'True'), ('false', 'False')],
        validators=[DataRequired(message="Use Sudo is a required field")])
    call_on = SelectField(
        'Call On',
        description=field_descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
