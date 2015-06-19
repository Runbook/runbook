######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Forms Class
######################################################################

from wtforms import Form
from wtforms import PasswordField
from wtforms.validators import Length, EqualTo


class ChangePassForm(Form):
    ''' Class that creates a Password Change Form '''

    old_password = PasswordField("Old Password")
    password = PasswordField(
        "Password",
        validators=[
            Length(min=8, message='Password must be a minimum of 8 characters'),
            EqualTo('confirm', message="Passwords did not match")
        ]
    )
    confirm = PasswordField("Repeat Password")


if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
