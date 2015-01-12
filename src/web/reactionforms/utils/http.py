"""Collection of HTTP utility classes and functions."""

from wtforms.validators import ValidationError


class HeaderList(object):
    """Custom wtforms validator for headers."""

    def __call__(self, form, field):
        try:
            for header in str.splitlines(str(field.data)):
                header = header.strip()
                # Ignore empty lines
                if not header:
                    continue
                key, value = header.split(':')
                key = key.strip()
                value = value.strip()
                assert key
                assert value
        except Exception, e:
            raise ValidationError('Invalid headers. Use key:value format.')
