######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired

from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Reaction form for the dashboard '''
    title = "AWS: Stop EC2 Instance"
    description = """
    <p>
    This reaction gives you the ability to stop any Amazon Web Services instance. When invoked this reaction utilizes the AWS API to request the specified instance be stopped.
    </p><p>
    A Simple use case for this reaction is to stop a system when capacity is no longer required. Another example is when performing a failover from a primary instance to a secondary instance.
    </p>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'region' : "us-west",
        'aws_access_key' : '123456789',
        'aws_secret_key' : 'abcdefghi',
        'instance_id' : '1000',
   })

    region = TextField(
        "AWS Region",
        description=BaseReactForm.descriptions['aws']['region'],
        validators=[DataRequired(message="AWS Region is a required field")])
    aws_access_key = TextField(
        "AWS Access Key",
        description=BaseReactForm.descriptions['aws']['accessKey'],
        validators=[DataRequired(message='AWS Access Key is a required field')])
    aws_secret_key = TextField(
        "AWS Secret Key",
        description=BaseReactForm.descriptions['aws']['accessSecretKey'],
        validators=[DataRequired(message='AWS Secret Key is a required field')])
    instance_id = TextField(
        "Instance ID",
        description=BaseReactForm.descriptions['aws']['instanceID'],
        validators=[DataRequired(message="Instance ID is a required field")])
    call_on = SelectField(
        "Call On",
        description=BaseReactForm.descriptions['callon'],
        choices=[
            ('false', 'False Monitors'),
            ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
