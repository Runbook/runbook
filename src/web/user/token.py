#####################################################################
# Runbook Web Application
# ------------------------------------------------------------------
# Generate and confirm an email confirmation token
#####################################################################


from itsdangerous import URLSafeTimedSerializer

from web import app


def generate_confirmation_token(email, expiration=3600):
    '''
    Given a user email address and expiration (in seconds),
    create a unique token.
    '''
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], expiration)
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    '''
    Given a token, as long as it has not expired an email will be returned.
    '''
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'])
    return email
