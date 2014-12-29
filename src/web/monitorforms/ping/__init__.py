######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Ping Health Check - Forms Class
######################################################################

from wtforms import TextField
from wtforms.validators import DataRequired, Regexp
from ..datacenter import DatacenterCheckForm


class CheckForm(DatacenterCheckForm):

    ''' Class that creates an Ping Health Check form for the dashboard '''
    pattern = "^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$"
    host = TextField(
        "host",
        validators=[
            DataRequired(message='Host is a required field and \
                                  should be a hostname or IP address'),
            Regexp(pattern, message="Invalid IP or Hostname format")
        ]
    )

if __name__ == '__main__':
    pass
