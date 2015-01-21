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

    api_key = TextField(
        "API Key",
        validators=[DataRequired(message='API Key is a required field')]
    )
    datacenter_id = TextField(
        "DatacenterID#",
        validators=[
            DataRequired(message='DatacenterID# is a required field'),
            NumberRange(
                min=1, max=None,
                message="DatacenterID should be a numeric ID number")
        ]
    )
    plan_id = TextField(
        "PlanID#",
        validators=[
            DataRequired(message='PlanID# is a required field'),
            NumberRange(
                min=1, max=None,
                message="PlanID should be a numeric ID number")
        ]
    )
    upper_limit = TextField(
        "Upper Limit",
        validators=[
            DataRequired(message='Upper Limit is a required field'),
            NumberRange(
                min=1, max=None,
                message="Upper Limit should be a number")
        ]
    )
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
