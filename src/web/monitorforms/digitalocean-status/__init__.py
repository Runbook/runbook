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

    choices = [
        ('new', 'New'),
        ('active', 'Active'),
        ('off', 'Off'),
        ('archive', 'Archive')
    ]

    apikey = TextField(
        'API Key',
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        'Droplet ID#',
        validators=[DataRequired(message='Droplet ID# is a required field'),
                    NumberRange(min=1, max=None,
                                message='Droplet ID should be a numeric ID number')])
    status = SelectMultipleField(
        'Status',
        choices=choices,
        validators=[DataRequired(message='Status is a required field')])

if __name__ == '__main__':
    pass
