######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(Form):
    ''' Class that creates signup form fields and validation '''

    email = TextField(
        "Email",
        validators=[Email(message='Email address invalid')])
    company = TextField(
        "Company",
        validators=[DataRequired(message='Company is a required field')])
    contact = TextField(
        "Contact",
        validators=[DataRequired(message='Contact Name is a required field')])
    password = PasswordField(
        "Password",
        validators=
        [
            Length(min=8, message='Password must be a minimum of 8 characters')
        ]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=
        [
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class LoginForm(Form):
    ''' Class that creates login form fields and validation '''

    email = TextField(
        "Email",
        validators=[Email(message='Email address invalid')])
    password = PasswordField(
        "Password",
        validators=[DataRequired(message='Password is required to login')])


class ChangePassForm(Form):
    ''' Class that creates a Password Change Form '''

    password = PasswordField(
        "Password",
        validators=
        [
            Length(min=8, message='Password must be a minimum of 8 characters'),
            EqualTo('confirm', message="Passwords did not match")
        ]
    )
    confirm = PasswordField("Repeat Password")


if __name__ == '__main__':
    pass
