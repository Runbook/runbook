"""Reactions form class for Twilio SMS Notification."""

from wtforms import SelectField, TextField
from wtforms.validators import DataRequired, Regexp
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    title = "Twilio: Send SMS"
    description = """
    <P> 
        This reaction is designed to use Twilio's API to send an SMS Message. This reaction can be used for simple SMS alerts and is similar to the Nexmo reaction.
    </P>
    """
    placeholders = BaseReactForm.placeholders
    placeholders.update({
        'account_sid' : 'AC12345',
        'auth_token' : '123456789',
        'from_address' : "Company125",
        'to_address' : "447525856424",
        'text' : "Alert: Something is not working",
    })
    descriptions=BaseReactForm.descriptions

    account_sid = TextField(
        'Account SID',
        description="Account SID provided by Twilio",
        validators=[DataRequired(message='Account SID is a required field.')])
    auth_token = TextField(
        'Authentication Token',
        description="Authentication Token used to authenticate with Twilio",
        validators=[DataRequired(message='Auth Token is a required field.')])
    from_address = TextField(
        'From Address',
        description="From address to send the SMS from",
        validators=[DataRequired(message='From Address is a required field.'),
                    Regexp('^\+?\d{5,}$', message='Invalid format for From Address. Use numbers only or international format (+123456789).')])
    to_address = TextField(
        'To Address',
        description="Address to send the SMS to",
        validators=[DataRequired(message='To Address is a required field.'),
                    Regexp('^\+?\d{5,}$', message='Invalid format for To Address. Use numbers only or international format (+123456789).')])
    text = TextField(
        'Message',
        description="Message to send within the SMS",
        validators=[DataRequired(message='Message Text is a required field.')])
    call_on = SelectField(
        "Call On",
        description=descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])


if __name__ == '__main__':
    pass
