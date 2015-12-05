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
    title = "Heroku: All Dyno Status"
    description = """
    This monitor will query the status of all Dynos associated with the specified Application. If any Dyno is not in an "up" or "idle" state this monitor will return False. If all Dynos have a healthy status this monitor will return True.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'appname' : 'Application Name',
    })
    apikey = TextField(
        "API Key",
        description=DatacenterCheckForm.descriptions['apikey'],
        validators=[DataRequired(
            message='API Key is a required field')])
    appname = TextField(
        "Application Name",
        description=DatacenterCheckForm.descriptions['heroku']['appname'],
        validators=[DataRequired(
            message='Application Name is a required field')])

if __name__ == '__main__':
    pass
