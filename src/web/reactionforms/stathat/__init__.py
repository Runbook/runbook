######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# CloudFlare IP Replacement - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, NumberRange
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''
    title = "StatHat Stat"
    description = """
    <P>
        This reaction provides the ability to call Stat Hat's API to increase a counter stat or send a defined value stat. This functionality allows users to create statistics based on Monitor results.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'stat_name' : 'Monitor True',
        'ez_key' : '123141231',
        'value' : '15',
    })
    descriptions=BaseReactForm.descriptions

    stat_name = TextField(
        "Stat Name",
        description="Define a name to use for the Stat",
        validators=[DataRequired(message='Stat Name is a required field')])
    ez_key = TextField(
        "EZ Key",
        description="Provide the API Key to use",
        validators=[DataRequired(message='EZ Key is a required field')])
    value = TextField(
        "Value",
        description="Provide the numeric value to send to StatHat.",
        validators=[NumberRange(message='Value must be a number')])
    continuous = SelectField(
        "Continuous",
        description="""
          Determine whether this stat should be sent for each reaction trigger, or only once
        """,
        choices=[('True', 'Yes'), ('False', 'No')],
        validators=[DataRequired(message='Continuous is a required field')])
    stat_type = SelectField(
        "Stat Type",
        description="Select a Stat Type to send",
        choices=[('count', 'Counter'), ('value', 'Value')],
        validators=[DataRequired(message='Stat Type is a required field')])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
