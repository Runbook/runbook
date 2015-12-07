######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Services Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''
    title = "Commando.io: Execute a Recipe on a Group of Servers"
    description = """
    <P>
      This reaction will trigger a "Recipe" execution across a Group of servers via Commando.io's API. For this reaction the server grouping and recipe should already be defined via Commando.io's interface.
    </P><P>
      For those already utilizing Commando.io's services this reaction allows you to execute predefined scripts or commands across groups of servers. These scripts can be as simple as restarting MySQL or as complicated as deploying an application. This reaction provides many possibilities for automated remediation.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'recipe_id' : '12345',
        'group_id' : 'Group01',
        'user' : 'user15',
   })


    recipe_id = TextField(
        "Recipe ID",
        description=BaseReactForm.descriptions['commando']['recipeID'],
        validators=[DataRequired(message='Recipe ID is a required field')])
    group_id = TextField(
        "Group ID",
        description=BaseReactForm.descriptions['commando']['groupID'],
        validators=[DataRequired(message='Group ID is a required field')])
    halt_on_stderr = SelectField(
        "Halt on Error",
        description=BaseReactForm.descriptions['commando']['haltonerror'],
        choices=[('false', 'False'), ('true', 'True')],
        validators=[DataRequired(message='Halt on Error is a required field')])
    user = TextField(
        "User ID",
        description=BaseReactForm.descriptions['commando']['userID'],
        validators=[DataRequired(message='User ID is a required field')])
    apikey = TextField(
        "API Key",
        description=BaseReactForm.descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field')])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
