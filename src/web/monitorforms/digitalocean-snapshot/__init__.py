######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Health Check - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import DataRequired, NumberRange
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Creates a wtforms form object for monitors '''

    apikey = TextField(
        "API Key",
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        "Droplet ID#",
        validators=[
            DataRequired(message='Droplet ID# is a required field'),
            NumberRange(min=1, max=None,
                        message="Droplet ID should be a numeric ID number")
        ]
    )


if __name__ == '__main__':
    pass
