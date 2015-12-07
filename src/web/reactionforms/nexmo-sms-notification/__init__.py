"""Reactions form class for Nexmo SMS Notification."""

from wtforms import SelectField, TextField
from wtforms.validators import DataRequired, Regexp
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    title = "Nexmo: Send SMS"
    description = """
    <P> 
        This reaction is designed to use Nexmo's API to send an SMS Message. This reaction can be used for simple SMS alerts and is similar to the Twilio reaction.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'api_key' : placeholders['apikey'],
        'api_secret' : "Secret API Key",
        'from_address' : "Company125",
        'to_address' : "447525856424",
        'text' : "Alert: Something is not working",
    })
    descriptions=BaseReactForm.descriptions

    api_key = TextField(
        'API Key',
        description=descriptions['apikey'],
        validators=[DataRequired(message='API Key is a required field.')])
    api_secret = TextField(
        'API Secret Key',
        description="""
           Provide Nexmo's secondary API Secret Key 
        """,
        validators=[DataRequired(message='API Secret is a required field.')])
    from_address = TextField(
        'From Address',
        description="""
            Specify a from address to use with the SMS message
        """,
        validators=[DataRequired(message='From Address is a required field.')])
    to_address = TextField(
        'To Address',
        description="""
            Specify the number to send the SMS message to in International format
        """,
        validators=[DataRequired(message='To Address is a required field.'),
                    Regexp('^\d{5,}$', message='Invalid format for To Address. Use numbers only.')])
    text = TextField(
        'Message Body',
        description="""
            Specify a message body for the SMS message
        """,
        validators=[DataRequired(message='Message Text is a required field.')])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
