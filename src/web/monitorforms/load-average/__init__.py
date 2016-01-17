from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Create a form class for monitor '''
    title = "1 Minute Load Average"
    description = """
    <p>This monitor opens an SSH connection to the specified server and checks whether the 1 minute load average is greater than the defined threshold. If the load average is beyond the threshold the monitor will return False, other wise this monitor will return True</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the monitor to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    <p>Success and Failure are determined by the ability to connect to the remote host, and the results from executed commands.</p>
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
        "SSH Username",
        description=DatacenterCheckForm.descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=DatacenterCheckForm.descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    threshold = TextField(
        "Threshold",
        description="""
          Define the maximum load average value to use as a threshold for detecting issues. For instance if a load average of 50 is unexpected simply put 50 in this field.
        """,
        validators=[
            DataRequired(message="Threshold required")
        ])

if __name__ == '__main__':
    pass
