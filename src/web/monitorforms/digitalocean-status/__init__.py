######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# DigitalOcean Droplet Status Check - Forms Class
######################################################################

from wtforms import TextField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Class that creates a DigitalOcean droplet status monitor form
    for the dashboard '''
    title = "DigitalOcean: Droplet Status"
    description = """
    This monitor will query DigitalOcean's API to identify the status of a specified Droplet. If the returned status matches the specified status the monitor is True. If the returned status does not match the specified status the monitor is False.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'dropletid' : '12345',
    })

    choices = [
        ('new', 'New'),
        ('active', 'Active'),
        ('off', 'Off'),
        ('archive', 'Archive')
    ]

    apikey = TextField(
        'API Key',
        description=DatacenterCheckForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        'Droplet ID#',
        description=DatacenterCheckForm.descriptions['digitalocean']['dropletid'],
        validators=[DataRequired(message='Droplet ID# is a required field'),
                    NumberRange(min=1, max=None,
                                message='Droplet ID should be a numeric ID number')])
    status = SelectMultipleField(
        'Status',
        description="""
        Select one or more status types that should define this monitor as True.
        """,
        choices=choices,
        validators=[DataRequired(message='Status is a required field')])

if __name__ == '__main__':
    pass
