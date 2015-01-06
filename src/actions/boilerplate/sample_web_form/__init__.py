# save this file/folder to /src/web/reactionforms/some-reaction


######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import DataRequired
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''

    field_name = TextField('Field Name', validators=[DataRequired()])


if __name__ == '__main__':
    pass
