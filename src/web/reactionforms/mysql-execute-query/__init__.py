"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    ''' Class that creates an form for the reaction '''
    title = "MySQL: Execute SQL Statement"
    description = """
    <p>This reaction will connect to a remote MySQL server and execute the specified SQL statement.</p>
    """
    placeholders = BaseReactForm.placeholders
    field_descriptions = BaseReactForm.descriptions
    placeholders.update({
        'server' : 'mysql.example.com',
        'user' : 'dbuser',
        'sql' : 'flush privileges',
    })

    server = TextField(
        "MySQL Server Address",
        description="""
          Specify a hostname or IP address to connect to.
        """,
        validators=[DataRequired(message='Server is a required field')])

    user = TextField(
        "Username",
        description="""
            Specify the MySQL user to connect with.
        """,
        validators=[DataRequired(message="Username is a required field")])

    password = TextField(
        "Password",
        description="""
            Specify the above MySQL user's password.
        """,
        validators=[DataRequired(message="Password is a required field")])

    sql = TextAreaField(
        "SQL Statement",
        description="""
            Specify the SQL statement to execute
        """,
        validators=[DataRequired(message='SQL Statement is a required field')])

    call_on = SelectField(
        'Call On',
        description=field_descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
