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
    title = "DigitalOcean: Recent Snapshot"
    description = """
    This monitor returns a True status if the specified Droplet has had a snapshot taken within the last 30 minutes.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'dropletid' : '12345',
    })

    apikey = TextField(
        "API Key",
        description=DatacenterCheckForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        "Droplet ID",
        description=DatacenterCheckForm.descriptions['digitalocean']['dropletid'],
        validators=[
            DataRequired(message='Droplet ID is a required field'),
            NumberRange(min=1, max=None,
                        message="Droplet ID should be a numeric ID number")
        ]
    )


if __name__ == '__main__':
    pass
