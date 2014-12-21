#####################################################################
# Runbook Web Application
# ------------------------------------------------------------------
# Generate and confirm an email confirmation token
#####################################################################


from itsdangerous import URLSafeTimedSerializer

from web import app


def generate_confirmation_token(email):
    '''
    Given a user email address, create a unique token.
    '''
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    '''
    Given a token and expiration (in seconds),
    as long as it has not expired an email will be returned.
    '''
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
