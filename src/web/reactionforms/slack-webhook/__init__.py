"""Reactions form class for slack notifications."""

from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):  #pylint: disable=no-init

    title = "Slack: Webhook"
    description = """
    <P>
      This reaction is designed to provide the ability to perform Incoming Webhooks to Slack channels. This functionality can be used to send notifications to Slack or even trigger Slack commands.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'channel' : '#general',
        'body' : 'Alert: Something happened',
        'url' : 'http://slack.com/adsaew112',
    })
    descriptions=BaseReactForm.descriptions

    url = TextField(
        'Webhook URL',
        description=descriptions['url'],
        validators=[DataRequired(message='The URL is a required field.'),
                    URL(message='Invalid URL Address.')])
    channel = TextField(
        'Channel',
        description="Specify the Channel to send the message to",
        validators=[DataRequired(message='Channel is a required field.')])
    body = TextField(
        'Message',
        description="Specify the message to send via the webhook",
        validators=[DataRequired(message='Message is a required field.')])
    call_on = SelectField(
        'Call On',
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])


if __name__ == '__main__':
    pass
