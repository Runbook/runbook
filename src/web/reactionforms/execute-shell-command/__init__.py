"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    ''' Class that creates an form for the reaction Execute Shell Command '''
    title = "Execute Shell Command"
    description = """
    <p>This reaction provides a method of executing an arbitrary shell command, script or series of commands on a remote host over SSH.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the reaction to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    """
    placeholders = BaseReactForm.placeholders

    host_string = TextField(
        "Target Host",
        description=BaseReactForm.descriptions['ssh']['host_string'],
        validators=[DataRequired(message='Target Host is a required field')])
    gateway = TextField(
        "Gateway Host",
        description=BaseReactForm.descriptions['ssh']['gateway'],
        validators=[Optional()])
    username = TextField(
        "Username",
        description=BaseReactForm.descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=BaseReactForm.descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    cmd = TextAreaField(
        "Command",
        description=BaseReactForm.descriptions['ssh']['cmd'],
        validators=[DataRequired(message='Command is a required field')])
    call_on = SelectField(
        'Call On',
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
