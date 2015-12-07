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
    title = "Linode: Create Node Server"
    description = """
    <P> 
        This reaction provides the ability create new Linode Node Servers. This reaction is similar to the DigitalOcean Create Droplet reaction and provides a simple way to increase infrastructure for environments that utilize automated provisioning tools.
    </P>
    <P>
        The Upper Limit field for this reaction works by querying the total number of Node Servers on an account and restricting the reaction from increasing the count beyond that number.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'linode_id' : '12345',
        'api_key' : placeholders['apikey'],
        'datacenter_id' : '2',
        'plan_id' : '2',
        'upper_limit' : '10',
    })
    descriptions=BaseReactForm.descriptions

    api_key = TextField(
        "API Key",
        description=descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')]
    )
    datacenter_id = TextField(
        "Datacenter ID#",
        description="""
          Specify the Datacenter you wish to place this Linode server. Common values: 2 (Dallas), 3 (Fremont), 7 (London).
        """,
        validators=[
            DataRequired(message='DatacenterID# is a required field'),
            NumberRange(
                min=1, max=None,
                message="DatacenterID should be a numeric ID number")
        ]
    )
    plan_id = TextField(
        "Plan ID#",
        description="""
          Specify the Plan ID you wish to create the Linode server against. Common values: 1 (1 CPU, $10), 2 (2 CPU, $20), 4 (4 CPU, $40)
        """,
        validators=[
            DataRequired(message='PlanID# is a required field'),
            NumberRange(
                min=1, max=None,
                message="PlanID should be a numeric ID number")
        ]
    )
    upper_limit = TextField(
        "Upper Limit",
        description="""
          Define an upper limit for the number of Linode Node Servers. This will check the total number of Node Servers and not increase the server count beyond that value.
        """,
        validators=[
            DataRequired(message='Upper Limit is a required field'),
            NumberRange(
                min=1, max=None,
                message="Upper Limit should be a number")
        ]
    )
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
