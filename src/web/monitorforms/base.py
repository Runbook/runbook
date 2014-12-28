######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Base Monitor Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, SelectMultipleField
from wtforms.validators import DataRequired


class BaseCheckForm(Form):

    ''' Class that creates an TCP Check form for the dashboard '''
    name = TextField(
        "Name",
        validators=[DataRequired(message='Name is a required field')]
    )
    reactions = SelectMultipleField("Reactions")

if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
