"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    ''' Class that creates an form for the reaction Docker: Start container '''
    title = "Docker: Start Container"
    description = """
    <p>This reaction will open an SSH connection to the specified host and execute the command <code>docker run -d {additional options} {image}</code>. The additional options field is optional, however it can be useful when assigning a name to the container such as adding <code>--name mycontainer</code>.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the reaction to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'image' : 'ubuntu:latest',
        'add_options' : '--name ubuntu',
    })
    field_descriptions = BaseReactForm.descriptions


    image = TextField(
        "Image",
        description=field_descriptions['docker']['image'],
        validators=[DataRequired(message='Image is a required field')])

    add_options = TextField(
        "Additional Options",
        description=field_descriptions['docker']['add_options'],
        validators=[Optional()])

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
