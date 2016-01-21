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
    title = "DigitalOcean: Assign/Re-Assign Floating IP"
    description = """
    <P>
      This reaction provides the ability to assign an existing Floating IP to the specified Droplet. If the floating IP is already assigned to a Droplet the IP will be un-assigned and re-assigned. 
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'dropletid' : '12345',
        'api_key' : placeholders['apikey'],
        'floatingip' : "10.0.0.1",
    })


    apikey = TextField(
        "API Key",
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    dropletid = TextField(
        "Droplet ID#",
        description=BaseReactForm.descriptions['digitalocean']['dropletid'],
        validators=[DataRequired(message='Droplet ID# is a required field'), NumberRange(min=1, max=None, message="Droplet ID should be a numeric ID number")])
    floatingip = TextField(
        "Floating IP",
        description="""
          Specify the Floating IP to re-assign.
        """,
        validators=[DataRequired(message='Floating IP is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
