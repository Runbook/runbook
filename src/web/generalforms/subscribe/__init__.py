######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, HiddenField
from wtforms.validators import NumberRange


class SubscribeForm(Form):

    ''' Class that creates signup form fields and validation '''
    stripeToken = HiddenField("stripeToken")


class AddPackForm(Form):

    ''' Class that creates signup form fields and validation '''
    add_packs = TextField(
        "Additional Monitor Packages",
        validators=[
            NumberRange(
                min=0,
                message="Additional Monitor Packages must be a number"
            )
        ])

if __name__ == '__main__':
    pass
