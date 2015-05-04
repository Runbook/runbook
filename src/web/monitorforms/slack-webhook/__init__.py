######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Health Check - Forms Class
######################################################################

from ..base import BaseCheckForm
from wtforms import TextField
from wtforms.validators import DataRequired


class CheckForm(BaseCheckForm):
    ''' Class that creates an web form for the dashboard '''
    token = TextField(
        'token',
        validators=[DataRequired(message='Slack Token is a required field')])

if __name__ == '__main__':
    pass
