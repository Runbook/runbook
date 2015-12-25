from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Class that creates an form for the monitor Execute Shell Command '''
    title = "Execute Shell Command"
    description = """
    <p>This monitor provides a method of executing an arbitrary shell command, script or series of commands on a remote host over SSH.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the monitor to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    <p>Success and Failure are determined by the ability to connect to the remote host, and the exit code provided from the commands executed. An exit code of 0 is a success, and any other exit code is a failure</p>
    """
    webhook_include = "monitors/webhooks/general.html"
    placeholders = DatacenterCheckForm.placeholders

    host_string = TextField(
        "Target Host",
        description=DatacenterCheckForm.descriptions['ssh']['host_string'],
        validators=[DataRequired(message='Target Host is a required field')])
    gateway = TextField(
        "Gateway Host",
        description=DatacenterCheckForm.descriptions['ssh']['gateway'],
        validators=[Optional()])
    username = TextField(
        "Username",
        description=DatacenterCheckForm.descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=DatacenterCheckForm.descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    cmd = TextAreaField(
        "Command",
        description=DatacenterCheckForm.descriptions['ssh']['cmd'],
        validators=[DataRequired(message='Command is a required field')])

if __name__ == '__main__':
    pass
