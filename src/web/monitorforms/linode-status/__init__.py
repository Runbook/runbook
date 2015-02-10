######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Linode Server Status Check - Forms Class
######################################################################

from wtforms import TextField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Class that creates a Linode server status monitor form
    for the dashboard '''

    choices = [
        (-2, 'Boot Failed (not in use)'),
        (-1, 'Being Created'),
        (0,  'Brand New'),
        (1,  'Running'),
        (2,  'Powered Off'),
        (3,  'Shutting Down (not in use)'),
        (4,  'Saved to Disk (not in use)')
    ]

    apikey = TextField(
        'API Key',
        validators=[DataRequired(message='API Key is a required field')])
    linodeid = TextField(
        'Linode ID#',
        validators=[DataRequired(message='Linode ID# is a required field'),
                    NumberRange(min=1, max=None,
                                message='Linode ID should be a numeric ID number')])
    status = SelectMultipleField(
        'Status',
        choices=choices,
        validators=[DataRequired(message='Status is a required field')])

if __name__ == '__main__':
    pass
