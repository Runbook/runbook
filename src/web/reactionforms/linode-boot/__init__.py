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
    title = "Linode: Boot Node Server"
    description = """
    <P> 
        This reaction provides the ability to Boot a specified Linode Node Server. This reaction simply sends a Boot API request to Linode. A simple use case for this functionality is to boot a cold standby system during failover.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'linode_id' : '12345',
        'api_key' : placeholders['apikey'],
    })
    descriptions=BaseReactForm.descriptions

    api_key = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    linode_id = TextField(
        "Linode ID#",
        description=descriptions['linode']['linodeID'],
        validators=[
            DataRequired(message='Linode ID# is a required field'),
            NumberRange(
                min=1, max=None,
                message="Linode ID should be a numeric ID number")
        ]
    )
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
