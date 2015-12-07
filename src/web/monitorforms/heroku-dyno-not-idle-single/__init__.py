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
    title = "Heroku: Dyno Not Idle"
    description = """
    This monitor returns false if a specified Heroku Dyno is in an Idle state. This monitor can be used to identify when Heroku Dynos should be scaled down or restarted.
    """
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'appname' : 'Application Name',
        'dynoname' : 'web',
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
    dynoname = TextField(
        "Dyno Name",
        description=DatacenterCheckForm.descriptions['heroku']['dynoname'],
        validators=[DataRequired(
            message='Dyno Name is a required field')])

if __name__ == '__main__':
    pass
