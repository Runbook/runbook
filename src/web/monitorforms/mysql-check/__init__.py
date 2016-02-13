from wtforms import TextField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Class that creates an form for the monitor Docker: Container is Running'''
    title = "MySQL: Status Check"
    description = """
    <p>This monitor opens a MySQL connection and executes a <code>show status</code> SQL statement. If the returned Value for the specified "Variable_name" exceeds the defined threshold the monitor will return False.</p>
    <p>The "Threshold Type" field allows you to define whether to trigger when the returned value is "Greater than" or "Less than" the threshold value.</p>
    <p>You can reference MySQL's documentation for a list of <a href="http://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html" target=_blank>Status Variables</a></p>
    """
    webhook_include = "monitors/webhooks/general.html"
    placeholders = DatacenterCheckForm.placeholders
    placeholders.update({
        'server' : 'mysql.example.com',
        'user' : 'dbuser',
        'status_variable' : 'Slow_queries'
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

    status_variable = TextField(
        "Status Variable",
        description="""
            Define the Status variable to check.
        """,
        validators=[DataRequired(message='Status Variable is a required field')])

    threshold_type = SelectField(
        "Threshold Type",
        description="""
          Define whether the threshold is triggered when the returned value is Greater than or Less than the defined threshold.
        """,
        choices=[('greater', 'Greater than'), ('less', 'Less than')],
        validators=[DataRequired(message='Threshold Type is a required field')])

    threshold = TextField(
        "Threshold",
        description="""
            Specify the threshold to trigger a false monitor on.
        """,
        validators=[DataRequired(message='Threshold is a required field')])

if __name__ == '__main__':
    pass
