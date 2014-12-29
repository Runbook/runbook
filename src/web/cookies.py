######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Cookies Class
######################################################################

from itsdangerous import TimestampSigner


def genCdata(uid, secretkey):
    s = TimestampSigner(secretkey)
    cookie = s.sign(uid)
    return cookie


def verifyCdata(cdata, secretkey, mxtime):
    s = TimestampSigner(secretkey)
    try:
        string = s.unsign(cdata, max_age=mxtime)
        return string
    except:
        return False


if __name__ == '__main__':  # pragma: no cover
    pass                    # pragma: no cover
