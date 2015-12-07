######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''
    title = "Rackspace: Reboot Server"
    description = """
    <P>
        This reaction provides the ability to Reboot a Rackspace hosted Cloud Server. The reboot API call is a graceful operation, for a forceful operation the Power Cycle reaction would be more appropriate.
    </P><P>
        This functionality can be used to reboot a server that is failing health checks. Within environments where servers are setup to restart services on boot this can be an easy issue remediation method.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'username' : 'User01',
        'serverid' : 'Server01',
    })
    descriptions=BaseReactForm.descriptions

    resource_choices = [
        ('cloudServersOpenStack', 'Next Generation Cloud Server'),
        ('cloudServers', 'First Generation Cloud Server')]

    region_choices = [
        ('DFW', 'DFW'),
        ('ORD', 'ORD'),
        ('IAD', 'IAD'),
        ('LON', 'LON'),
        ('SYD', 'SYD'),
        ('HKG', 'HKG')]

    username = TextField(
        "Username",
        description=descriptions['username'],
        validators=[DataRequired(message='Username is a required field')])
    apikey = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    serverid = TextField(
        "Server ID#",
        description=descriptions['rackspace']['serverID'],
        validators=[DataRequired(message='Server ID# is a required field')])
    region = SelectField(
        "Region",
        description=descriptions['rackspace']['region'],
        choices=region_choices,
        validators=[DataRequired(message="Select a Region")])
    resource_type = SelectField(
        "Server Type",
        description=descriptions['rackspace']['resourceType'],
        choices=resource_choices,
        validators=[DataRequired(message="Select a Server Type")])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
