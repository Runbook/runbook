from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Class that creates an form for the monitor Docker: Container is Running'''
    title = "Docker: Container is Running"
    description = """
    <p>This monitor opens an SSH connection to the specified server and checks whether the specified Docker container is running.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the monitor to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    <p>Success and Failure are determined by the ability to connect to the remote host, and the results from executed Docker commands. If the Docker commands require <code>sudo</code> to be used, simply specify True on the "use Sudo" field.</p>
    """
    webhook_include = "monitors/webhooks/general.html"
    placeholders = DatacenterCheckForm.placeholders

    container_name = TextField(
        "Container Name",
        description=DatacenterCheckForm.descriptions['docker']['container_name'],
        validators=[DataRequired(message='Container is a required field')])
    host_string = TextField(
        "Target Host",
        description=DatacenterCheckForm.descriptions['ssh']['host_string'],
        validators=[DataRequired(message='Target Host is a required field')])
    gateway = TextField(
        "Gateway Host",
        description=DatacenterCheckForm.descriptions['ssh']['gateway'],
        validators=[Optional()])
    username = TextField(
        "SSH Username",
        description=DatacenterCheckForm.descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=DatacenterCheckForm.descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    use_sudo = SelectField(
        "Use Sudo",
        description=DatacenterCheckForm.descriptions['ssh']['use_sudo'],
        choices=[('true', 'True'), ('false', 'False')],
        validators=[DataRequired(message="Use Sudo is a required field")])

if __name__ == '__main__':
    pass
