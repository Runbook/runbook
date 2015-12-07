######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################


from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, NumberRange
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''
    title = "DigitalOcean: Create Snapshot"
    description = """
    <P>
      This reaction is design to allow users to automatically create a Snapshot of a DigitalOcean Droplet. The functionality of snapshots allow users to capture a server's configuration and state at a given time. These snapshots could be used for backups or provisioning of new servers at a later time.
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
        'snapname' : 'FancyNewSnapshot',
    })

    apikey = TextField(
        "API Key",
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        "Droplet ID#",
        description=BaseReactForm.descriptions['digitalocean']['dropletid'],
        validators=[DataRequired(message='Droplet ID# is a required field'), NumberRange(min=1, max=None, message="Droplet ID should be a numeric ID number")])
    snapname = TextField(
        "Snapshot Name",
        description="""
        Specify the desired name of the snapshot.
        """,
        validators=[DataRequired(message='Snapshot Name is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
