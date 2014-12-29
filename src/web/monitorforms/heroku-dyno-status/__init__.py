######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Health Check - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import DataRequired
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Creates a wtforms form object for monitors '''
    apikey = TextField(
        "API Key",
        validators=[DataRequired(
            message='API Key is a required field')])
    appname = TextField(
        "Application Name", validators=[DataRequired(
            message='Application Name is a required field')])

if __name__ == '__main__':
    pass
