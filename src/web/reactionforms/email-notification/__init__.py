"""Reactions form class for email notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Email
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    title = "Email Notification"
    description = """
    <P>
      This reaction provides basic Email Notification ability. This reaction will send the specified email each time it is executed.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'to_address' : 'email@example.com',
        'body' : "Help!",
        'subject' : "Alert: Runbook monitor triggered event",
    })

    to_address = TextField(
        'To Address',
        description="""
            Provide a basic email address to send the email notification to.
        """,
        validators=[DataRequired(message='To Address is a required field.'),
                    Email(message='Invalid Email Address.')])
    subject = TextField(
        'Subject',
        description="""
            Provide a subject to be used as the subject of the email.
        """,
        validators=[DataRequired(message='Subject is a required field.')])
    body = TextAreaField(
        'Message Body',
        description="""
            Provide the body of the email to be sent.
        """,
        validators=[DataRequired(message='Body is a required field.')])
    call_on = SelectField(
        'Call On',
        description=BaseReactForm.descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
